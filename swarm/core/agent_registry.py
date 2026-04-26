"""
Agent Registry — skill-based discovery.

Agents register when they start; the registry returns the best available match
for a set of required skills. Also supports pausing, resuming, and killing.
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# Canonical skill tags used across the system
KNOWN_SKILLS = {
    "research":    "Researcher",
    "plan":        "Planner",
    "code":        "Coder / Builder",
    "verify":      "Verifier",
    "debug":       "Debugger",
    "design":      "Designer",
    "spawn_agent": "Builder (meta)",
}


@dataclass
class AgentInfo:
    name: str
    skills: list[str]
    port: int
    status: str = "idle"           # idle | busy | paused | offline
    pid: Optional[int] = None
    current_task: Optional[str] = None
    registered_at: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    spawned: bool = False          # True = dynamically created
    miss_count: int = 0            # missed heartbeats

    def score(self, required_skills: list[str]) -> float:
        """Overlap score 0..1 — higher is better."""
        if not required_skills:
            return 1.0
        my     = set(self.skills)
        needed = set(required_skills)
        inter  = my & needed
        if not inter:
            return 0.0
        return len(inter) / len(needed)

    def to_dict(self) -> dict:
        return {
            "name":          self.name,
            "skills":        self.skills,
            "port":          self.port,
            "status":        self.status,
            "pid":           self.pid,
            "current_task":  self.current_task,
            "registered_at": self.registered_at,
            "last_seen":     self.last_seen,
            "spawned":       self.spawned,
            "miss_count":    self.miss_count,
        }


class AgentRegistry:
    """
    Central registry for all swarm agents.
    Thread-safe. Supports skill-based discovery, health tracking, pause/resume.
    """

    STALE_SEC = 20   # mark offline if no heartbeat for this long

    def __init__(self):
        self._lock   = threading.RLock()
        self._agents: dict[str, AgentInfo] = {}
        self._log:    list[dict]           = []

    # ── Lifecycle ─────────────────────────────────────────────────────────────

    def register(self, name: str, skills: list[str], port: int, spawned: bool = False) -> AgentInfo:
        with self._lock:
            info = AgentInfo(name=name, skills=skills, port=port, spawned=spawned)
            self._agents[name] = info
            self._emit("registered", name, {"skills": skills, "port": port})
            return info

    def unregister(self, name: str) -> None:
        with self._lock:
            self._agents.pop(name, None)
            self._emit("unregistered", name, {})

    def heartbeat(
        self,
        name: str,
        status: str,
        pid: int | None = None,
        task: str | None = None,
    ) -> None:
        with self._lock:
            a = self._agents.get(name)
            if a:
                a.last_seen   = time.time()
                a.miss_count  = 0
                a.status      = status
                if pid  is not None: a.pid          = pid
                if task is not None: a.current_task = task

    def tick_health(self) -> list[str]:
        """Call periodically. Returns names of agents now marked offline."""
        offline = []
        with self._lock:
            now = time.time()
            for a in self._agents.values():
                if a.status == "offline":
                    continue
                age = now - a.last_seen
                if age > self.STALE_SEC:
                    a.miss_count += 1
                    a.status      = "offline"
                    offline.append(a.name)
                    self._emit("offline", a.name, {"age_sec": round(age)})
        return offline

    # ── Control ───────────────────────────────────────────────────────────────

    def pause(self, name: str) -> bool:
        with self._lock:
            a = self._agents.get(name)
            if a and a.status not in ("offline", "paused"):
                a.status = "paused"
                self._emit("paused", name, {})
                return True
            return False

    def resume(self, name: str) -> bool:
        with self._lock:
            a = self._agents.get(name)
            if a and a.status == "paused":
                a.status = "idle"
                self._emit("resumed", name, {})
                return True
            return False

    def mark_busy(self, name: str, task_desc: str) -> None:
        with self._lock:
            a = self._agents.get(name)
            if a:
                a.status       = "busy"
                a.current_task = task_desc[:80]

    def mark_idle(self, name: str) -> None:
        with self._lock:
            a = self._agents.get(name)
            if a and a.status == "busy":
                a.status       = "idle"
                a.current_task = None

    # ── Discovery ─────────────────────────────────────────────────────────────

    def best_for(self, required_skills: list[str]) -> Optional[AgentInfo]:
        """Return the highest-scoring idle agent, or None."""
        with self._lock:
            candidates = [a for a in self._agents.values() if a.status == "idle"]
            if not candidates:
                return None
            ranked = sorted(candidates, key=lambda a: a.score(required_skills), reverse=True)
            best = ranked[0]
            return best if best.score(required_skills) > 0 else None

    def missing_skills(self, required_skills: list[str]) -> list[str]:
        """Return skills that NO agent (any status) currently covers."""
        with self._lock:
            covered = set()
            for a in self._agents.values():
                covered.update(a.skills)
            return [s for s in required_skills if s not in covered]

    def all_agents(self) -> list[dict]:
        with self._lock:
            return [a.to_dict() for a in self._agents.values()]

    def get(self, name: str) -> Optional[AgentInfo]:
        with self._lock:
            return self._agents.get(name)

    # ── Events ────────────────────────────────────────────────────────────────

    def get_events(self, since: float = 0.0) -> list[dict]:
        with self._lock:
            return [e for e in self._log if e["ts"] > since]

    def _emit(self, event: str, name: str, data: dict) -> None:
        self._log.append({"ts": time.time(), "event": event, "agent": name, **data})
        if len(self._log) > 300:
            self._log = self._log[-300:]


# Process-wide singleton
shared_registry = AgentRegistry()
