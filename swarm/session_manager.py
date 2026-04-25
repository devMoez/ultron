"""
SessionManager — owns parallel multi-session task execution for Ultron swarm.

Lifecycle:
    user prompt
        │
        ├─ route_prompt() ──► classify NEW | EDIT | CLARIFY (router_llm)
        │                          │
        │     EDIT ◄───────────────┘
        │       └─ amend_session(): hybrid — interrupt builder/debugger,
        │                          append for planner/designer/verifier
        │     NEW
        │       └─ create_session(): spawn pipeline if capacity, else queue
        │
        └─ MAX_SESSIONS gate (default 5, FIFO overflow)

Persistence: in-memory only for fast path; the underlying tasks land in the
existing SQLite DB via the orchestrator's /assign_task path, so durability
matches today's behavior.
"""
from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable

import httpx

from swarm_config import (
    AGENT_PORTS, APPEND_ONLY_AGENTS, MAX_SESSIONS, SOFT_INTERRUPT_AGENTS,
    TASKS_QUEUE,
)
from router_llm import classify, RouteResult

log = logging.getLogger("session_manager")


SessionStatus = str  # "queued" | "active" | "paused" | "done" | "failed" | "cancelled"


@dataclass
class Amendment:
    text: str
    submitted_at: float
    delivered: bool = False
    delivery_mode: str = ""        # "soft_interrupt" | "append_only"


@dataclass
class Session:
    id: str
    prompt: str
    status: SessionStatus = "queued"
    current_agent: str | None = None
    task_ids: list[int] = field(default_factory=list)
    amendments: list[Amendment] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    started_at: float | None = None
    finished_at: float | None = None
    project_path: str = ""
    target_agent: str = "planner"
    last_result: str = ""
    error: str = ""

    def to_public(self) -> dict[str, Any]:
        return {
            "id":            self.id,
            "prompt":        self.prompt,
            "status":        self.status,
            "current_agent": self.current_agent,
            "task_ids":      list(self.task_ids),
            "amendments":    [{"text": a.text, "submitted_at": a.submitted_at,
                               "delivered": a.delivered, "mode": a.delivery_mode}
                              for a in self.amendments],
            "created_at":    self.created_at,
            "started_at":    self.started_at,
            "finished_at":   self.finished_at,
            "project_path":  self.project_path,
            "target_agent":  self.target_agent,
            "last_result":   self.last_result[:500] if self.last_result else "",
            "error":         self.error,
        }


class SessionManager:
    """Thread-safe coordinator for up to MAX_SESSIONS concurrent pipelines."""

    def __init__(self, max_sessions: int = MAX_SESSIONS):
        self.max_sessions = max_sessions
        self._sessions: dict[str, Session] = {}
        self._pending: deque[str] = deque()      # session ids waiting for a slot
        self._lock = threading.RLock()

        # Hook injected by orchestrator: how to actually dispatch a task to an
        # agent. Signature: (session_id, agent, description, project_path) -> task_id|None
        self.dispatch_hook: Callable[[str, str, str, str], int | None] | None = None

    # ── Public API ────────────────────────────────────────────────────────────

    def route_prompt(
        self,
        prompt: str,
        project_path: str = "",
        target_agent: str = "planner",
    ) -> dict[str, Any]:
        """Main entry. Classify and either create or amend a session."""
        with self._lock:
            actives = [s.to_public() for s in self._sessions.values()
                       if s.status in ("queued", "active", "paused")]

        result = classify(prompt, actives)
        log.info(f"Router decision: {result.decision} "
                 f"(target={result.target_session_id}, conf={result.confidence:.2f}, "
                 f"fallback={result.used_fallback})")

        if result.decision == "EDIT" and result.target_session_id:
            outcome = self.amend_session(result.target_session_id, prompt)
            outcome["routing"] = self._routing_meta(result)
            return outcome

        if result.decision == "CLARIFY":
            return {
                "ok":       False,
                "needs_clarification": True,
                "message":  "Ambiguous: could be a new task or an edit to a running one.",
                "routing":  self._routing_meta(result),
                "active":   actives,
            }

        # NEW
        return self.create_session(
            prompt=prompt,
            project_path=project_path,
            target_agent=target_agent,
            routing=self._routing_meta(result),
        )

    def create_session(
        self,
        prompt: str,
        project_path: str = "",
        target_agent: str = "planner",
        routing: dict | None = None,
    ) -> dict[str, Any]:
        sid = uuid.uuid4().hex[:12]
        sess = Session(
            id=sid,
            prompt=prompt,
            project_path=project_path,
            target_agent=target_agent,
        )
        with self._lock:
            self._sessions[sid] = sess
            active_count = sum(1 for s in self._sessions.values()
                               if s.status in ("active", "paused"))
            if active_count >= self.max_sessions:
                self._pending.append(sid)
                position = len(self._pending)
                log.info(f"Session {sid} queued at position {position} "
                         f"(active={active_count}/{self.max_sessions})")
                return {
                    "ok":           True,
                    "session_id":   sid,
                    "status":       "queued",
                    "queue_pos":    position,
                    "active_count": active_count,
                    "routing":      routing or {},
                }
            self._launch_locked(sess)

        return {
            "ok":         True,
            "session_id": sid,
            "status":     "active",
            "routing":    routing or {},
        }

    def amend_session(self, session_id: str, text: str) -> dict[str, Any]:
        """All amendments are routed through the planner.

        The manager doesn't decide *how* to apply an edit — it hands the
        planner a re-plan task that includes the original prompt, the
        current agent, the latest result, and the new amendment text.
        Planner decides: redirect, re-plan, inject, or no-op, then
        forwards to the appropriate agent itself.
        """
        with self._lock:
            sess = self._sessions.get(session_id)
            if not sess:
                return {"ok": False, "error": f"session {session_id} not found"}
            if sess.status in ("done", "failed", "cancelled"):
                # Session already finished — escalate to a NEW one with merged context.
                merged = f"{sess.prompt}\n\n[Follow-up]\n{text}"
                return self.create_session(
                    prompt=merged,
                    project_path=sess.project_path,
                    target_agent=sess.target_agent,
                    routing={"merged_from": session_id, "reason": "previous session finished"},
                )

            amend = Amendment(text=text, submitted_at=time.time(),
                              delivery_mode="planner_replan")
            sess.amendments.append(amend)
            current_agent = sess.current_agent
            snapshot = {
                "id":            sess.id,
                "prompt":        sess.prompt,
                "current_agent": current_agent,
                "task_ids":      list(sess.task_ids),
                "last_result":   sess.last_result,
                "project_path":  sess.project_path,
            }

        # Drop a planner task into the queue. The orchestrator's existing
        # watcher will pick it up, route to planner, and the planner will
        # forward to the right agent.
        delivered = self._dispatch_planner_amendment(snapshot, text)
        with self._lock:
            amend.delivered = delivered

        # Optional fallback: if the running agent is one of the configured
        # SOFT_INTERRUPT_AGENTS AND the user opted into hybrid mode via env,
        # also poke that agent so it can pause early. Off by default.
        if current_agent in SOFT_INTERRUPT_AGENTS:
            self._deliver_amendment(self._sessions[session_id], amend)

        log.info(f"Amendment to {session_id} → planner re-plan (delivered={delivered}): {text[:80]}")
        return {
            "ok":           True,
            "session_id":   session_id,
            "mode":         "planner_replan",
            "delivered":    delivered,
            "current_agent": current_agent,
        }

    def _dispatch_planner_amendment(self, snap: dict, amend_text: str) -> bool:
        """Write a planner task that asks it to re-plan an existing session."""
        try:
            description = (
                f"[AMENDMENT TO ACTIVE SESSION {snap['id']}]\n\n"
                f"ORIGINAL PROMPT:\n{snap['prompt']}\n\n"
                f"CURRENTLY AT AGENT: {snap['current_agent'] or '(none)'}\n"
                f"LATEST PARTIAL RESULT:\n{(snap['last_result'] or '(none)')[:1500]}\n\n"
                f"USER NOW ASKS:\n{amend_text}\n\n"
                f"INSTRUCTIONS FOR PLANNER:\n"
                f"  1. Decide if this is a redirection (different agent), a refinement "
                f"(same agent, new spec), or a chained extension (after current finishes).\n"
                f"  2. Output a short plan and forward the next step to the appropriate agent "
                f"via /call/<agent>. Reuse session_id={snap['id']} in the forwarded payload."
            )
            task = {
                "session_id":   snap["id"],
                "target_agent": "planner",
                "description":  description,
                "project_path": snap["project_path"],
                "kind":         "amendment",
                "submitted_at": time.time(),
                "source":       "session-manager-amend",
            }
            TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
            fname = TASKS_QUEUE / f"amend_{snap['id']}_{uuid.uuid4().hex[:6]}.json"
            fname.write_text(json.dumps(task, indent=2), encoding="utf-8")
            return True
        except Exception as e:
            log.error(f"Failed to write planner amend task: {e}")
            return False

    def cancel_session(self, session_id: str) -> dict[str, Any]:
        with self._lock:
            sess = self._sessions.get(session_id)
            if not sess:
                return {"ok": False, "error": "not found"}
            if sess.status in ("done", "failed", "cancelled"):
                return {"ok": True, "already": sess.status}
            sess.status = "cancelled"
            sess.finished_at = time.time()
            try:
                self._pending.remove(session_id)
            except ValueError:
                pass
        # Tell the active agent to drop the work (best effort).
        try:
            self._notify_agent_cancel(sess)
        except Exception as e:
            log.warning(f"cancel notify failed: {e}")
        self._maybe_promote_pending()
        return {"ok": True, "session_id": session_id, "status": "cancelled"}

    def list_sessions(self) -> list[dict[str, Any]]:
        with self._lock:
            return [s.to_public() for s in self._sessions.values()]

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            sess = self._sessions.get(session_id)
            return sess.to_public() if sess else None

    def mark_session_done(
        self,
        task_id: int,
        success: bool,
        result: str,
    ) -> str | None:
        """Called by orchestrator when a task finishes. Returns session_id if matched."""
        with self._lock:
            for sess in self._sessions.values():
                if task_id in sess.task_ids:
                    sess.last_result = result or ""
                    if not success:
                        sess.status = "failed"
                        sess.error = result or ""
                        sess.finished_at = time.time()
                    else:
                        # Naive completion model: a task finishing on the
                        # session's terminal agent (verifier) ends the session.
                        if sess.current_agent == "verifier":
                            sess.status = "done"
                            sess.finished_at = time.time()
                    sid = sess.id
                    break
            else:
                return None
        if self._sessions[sid].status in ("done", "failed", "cancelled"):
            self._maybe_promote_pending()
        return sid

    def attach_task(self, session_id: str, task_id: int, agent: str) -> None:
        with self._lock:
            sess = self._sessions.get(session_id)
            if not sess:
                return
            if task_id not in sess.task_ids:
                sess.task_ids.append(task_id)
            sess.current_agent = agent
            if sess.started_at is None:
                sess.started_at = time.time()
                sess.status = "active"

    # ── Internals ─────────────────────────────────────────────────────────────

    def _routing_meta(self, r: RouteResult) -> dict:
        return {
            "decision":    r.decision,
            "target":      r.target_session_id,
            "reason":      r.reason,
            "confidence":  r.confidence,
            "fallback":    r.used_fallback,
        }

    def _launch_locked(self, sess: Session) -> None:
        """Caller must hold self._lock. Drops a task file in the queue dir
        OR calls the dispatch_hook if registered. We prefer the queue path so
        the orchestrator's existing watcher takes over and DB inserts happen
        in the canonical place."""
        sess.status = "active"
        sess.current_agent = sess.target_agent
        sess.started_at = time.time()

        task = {
            "session_id":   sess.id,
            "target_agent": sess.target_agent,
            "description":  _embed_amendments(sess),
            "project_path": sess.project_path,
            "submitted_at": time.time(),
            "source":       "session-manager",
        }
        TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
        fname = TASKS_QUEUE / f"sess_{sess.id}_{uuid.uuid4().hex[:6]}.json"
        fname.write_text(json.dumps(task, indent=2), encoding="utf-8")
        log.info(f"Session {sess.id} launched → queue file {fname.name}")

    def _maybe_promote_pending(self) -> None:
        with self._lock:
            active_count = sum(1 for s in self._sessions.values()
                               if s.status in ("active", "paused"))
            while self._pending and active_count < self.max_sessions:
                next_id = self._pending.popleft()
                sess = self._sessions.get(next_id)
                if not sess or sess.status != "queued":
                    continue
                self._launch_locked(sess)
                active_count += 1
                log.info(f"Promoted queued session {next_id} → active")

    def _deliver_amendment(self, sess: Session, amend: Amendment) -> bool:
        """Send amendment to the running agent. Returns True if delivered.
        For append-only agents we still POST it — the agent decides when to
        consume it based on its own policy."""
        agent = sess.current_agent
        if not agent:
            return False
        port = AGENT_PORTS.get(agent)
        if not port:
            return False
        try:
            with httpx.Client(timeout=3.0) as c:
                r = c.post(
                    f"http://127.0.0.1:{port}/amend",
                    json={
                        "session_id":   sess.id,
                        "text":         amend.text,
                        "mode":         amend.delivery_mode,
                        "submitted_at": amend.submitted_at,
                    },
                )
                return r.status_code == 200
        except Exception as e:
            log.debug(f"amend delivery to {agent} failed: {e}")
            return False

    def _notify_agent_cancel(self, sess: Session) -> None:
        agent = sess.current_agent
        if not agent:
            return
        port = AGENT_PORTS.get(agent)
        if not port:
            return
        try:
            with httpx.Client(timeout=3.0) as c:
                c.post(f"http://127.0.0.1:{port}/cancel",
                       json={"session_id": sess.id})
        except Exception:
            pass


def _embed_amendments(sess: Session) -> str:
    """Render the description sent to the first agent.
    On launch there are no amendments yet — but if a session is being
    re-launched after cancel/restart this preserves them."""
    if not sess.amendments:
        return sess.prompt
    addenda = "\n".join(f"- {a.text}" for a in sess.amendments)
    return f"{sess.prompt}\n\n[Amendments]\n{addenda}"
