"""
LLM-based prompt router.

Given a new user prompt and the list of currently active sessions, decides:
  - NEW            → start a fresh parallel session
  - EDIT:<id>      → amendment to an existing session
  - CLARIFY        → ambiguous, ask the user

The classifier uses an OpenAI-compatible chat-completions endpoint
(OpenRouter / DeepSeek / local). If the API call fails or no key is
configured, falls back to a heuristic classifier so the swarm keeps
working offline.
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Iterable, Literal

import httpx

from swarm_config import (
    ROUTER_API_KEY, ROUTER_BASE_URL, ROUTER_MODEL,
    ROUTER_PROVIDER, ROUTER_TIMEOUT_SEC,
)

log = logging.getLogger("router_llm")

Decision = Literal["NEW", "EDIT", "CLARIFY"]


@dataclass
class RouteResult:
    decision: Decision
    target_session_id: str | None = None     # set when decision == "EDIT"
    reason: str = ""
    confidence: float = 0.0
    used_fallback: bool = False


SYSTEM_PROMPT = """You are a routing classifier for a multi-agent task system.

You are given:
  1. A list of active sessions (each has id, original prompt, status).
  2. A new user prompt that just arrived.

Decide ONE of:
  - "NEW"            → the new prompt is a separate, unrelated task.
  - "EDIT:<id>"      → the new prompt modifies, amends, clarifies, or extends one of the active sessions.
  - "CLARIFY"        → genuinely ambiguous; need to ask the user.

Rules:
  - If the new prompt mentions the same files, features, project, or domain
    as an active session, prefer EDIT.
  - Phrases like "also", "instead", "wait", "change", "but make it", "add to that",
    "the one we just" strongly imply EDIT.
  - Completely unrelated topic, technology, or project → NEW.
  - If two active sessions could match, pick the most recent.
  - Return STRICT JSON only. No prose. Schema:
    {"decision": "NEW" | "EDIT" | "CLARIFY", "session_id": "<id or null>", "reason": "<short>", "confidence": <0..1>}
"""


def classify(
    new_prompt: str,
    active_sessions: Iterable[dict],
) -> RouteResult:
    """Classify a new prompt against active sessions.

    active_sessions: iterable of dicts shaped like
        {"id": "...", "prompt": "...", "status": "...", "current_agent": "..."}
    """
    sessions_list = list(active_sessions)

    # Cheap fast path: nothing running → always NEW.
    if not sessions_list:
        return RouteResult(decision="NEW", reason="no active sessions")

    if not ROUTER_API_KEY:
        log.warning("Router LLM has no API key — using heuristic fallback")
        return _heuristic(new_prompt, sessions_list)

    try:
        return _llm_call(new_prompt, sessions_list)
    except Exception as e:
        log.warning(f"Router LLM failed ({e}) — using heuristic fallback")
        return _heuristic(new_prompt, sessions_list)


# ── LLM path ──────────────────────────────────────────────────────────────────

def _llm_call(new_prompt: str, sessions: list[dict]) -> RouteResult:
    user_blob = {
        "active_sessions": [
            {
                "id":            s.get("id"),
                "prompt":        (s.get("prompt") or "")[:300],
                "status":        s.get("status"),
                "current_agent": s.get("current_agent"),
            }
            for s in sessions
        ],
        "new_prompt": new_prompt,
    }

    headers = {
        "Authorization": f"Bearer {ROUTER_API_KEY}",
        "Content-Type":  "application/json",
    }
    if ROUTER_PROVIDER == "openrouter":
        headers["HTTP-Referer"] = "https://github.com/ultron-swarm"
        headers["X-Title"]      = "Ultron Swarm Router"

    body = {
        "model":       ROUTER_MODEL,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": json.dumps(user_blob, ensure_ascii=False)},
        ],
    }

    with httpx.Client(timeout=ROUTER_TIMEOUT_SEC) as client:
        r = client.post(f"{ROUTER_BASE_URL}/chat/completions", json=body, headers=headers)
        r.raise_for_status()
        payload = r.json()

    content = payload["choices"][0]["message"]["content"]
    parsed = _parse_json_loose(content)

    decision = parsed.get("decision", "NEW").upper()
    session_id = parsed.get("session_id") or None
    if decision not in ("NEW", "EDIT", "CLARIFY"):
        decision = "NEW"
    if decision == "EDIT" and not session_id:
        # Model said EDIT but didn't pick an id — fall back to most-recent
        session_id = sessions[-1].get("id")

    return RouteResult(
        decision=decision,                # type: ignore[arg-type]
        target_session_id=session_id if decision == "EDIT" else None,
        reason=str(parsed.get("reason", ""))[:200],
        confidence=float(parsed.get("confidence", 0.0) or 0.0),
        used_fallback=False,
    )


def _parse_json_loose(text: str) -> dict:
    """Strip code fences / extract first {...} block, then json-load."""
    text = text.strip()
    # remove ``` fences if present
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    # try direct parse, else find first {...}
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise


# ── Heuristic fallback ────────────────────────────────────────────────────────

_EDIT_HINTS = re.compile(
    r"\b(also|instead|wait|actually|change|modify|update|add to (it|that|the)|"
    r"but make|but it|fix that|the (one|task|thing) (you|i|we) (just|are|were)|"
    r"on top of|same|previous|earlier)\b",
    re.IGNORECASE,
)


def _heuristic(new_prompt: str, sessions: list[dict]) -> RouteResult:
    """No-LLM fallback. Looks for edit-hint words + token overlap."""
    has_edit_hint = bool(_EDIT_HINTS.search(new_prompt))

    new_tokens = _tokens(new_prompt)
    best: tuple[float, dict | None] = (0.0, None)
    for s in sessions:
        overlap = _jaccard(new_tokens, _tokens(s.get("prompt") or ""))
        if overlap > best[0]:
            best = (overlap, s)

    overlap, target = best
    if has_edit_hint and target is not None and overlap >= 0.05:
        return RouteResult(
            decision="EDIT",
            target_session_id=target.get("id"),
            reason=f"heuristic: edit-hint + overlap={overlap:.2f}",
            confidence=min(0.7, 0.4 + overlap),
            used_fallback=True,
        )
    if overlap >= 0.35 and target is not None:
        return RouteResult(
            decision="EDIT",
            target_session_id=target.get("id"),
            reason=f"heuristic: high overlap={overlap:.2f}",
            confidence=overlap,
            used_fallback=True,
        )
    return RouteResult(
        decision="NEW",
        reason=f"heuristic: no edit signal (best overlap={overlap:.2f})",
        confidence=1.0 - overlap,
        used_fallback=True,
    )


_WORD = re.compile(r"[A-Za-z][A-Za-z0-9_]+")
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "for", "on",
    "with", "is", "it", "this", "that", "be", "as", "at", "by", "from",
    "i", "you", "we", "they", "me", "my", "your", "make", "do", "want",
    "please", "can", "should", "would", "could", "will", "have", "has",
}


def _tokens(text: str) -> set[str]:
    return {w.lower() for w in _WORD.findall(text or "") if w.lower() not in _STOPWORDS}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0
