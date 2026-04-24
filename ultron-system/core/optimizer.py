"""Phase 12 — Optimizer: model routing, agent allocation, behavior prediction."""
import json
import time
import threading
from collections import defaultdict
from pathlib import Path
from core.config import MEMORY_DIR
from core.logger import get_logger

log = get_logger("optimizer")

OPT_DIR  = MEMORY_DIR / "shared" / "optimizer"
OPT_DIR.mkdir(parents=True, exist_ok=True)
BEHAVIOR_LOG = OPT_DIR / "behavior.jsonl"

_lock = threading.Lock()

# ── Model routing table ───────────────────────────────────────────────────────

MODEL_ROUTING = {
    "code":      "deepseek-r1",
    "debug":     "deepseek-r1",
    "design":    "llama3-70b",
    "plan":      "llama3-70b",
    "research":  "llama3-70b",
    "verify":    "llama3-70b",
    "chat":      "llama3-8b-instant",
    "quick":     "llama3-8b-instant",
    "default":   "llama3-70b",
}

AGENT_ROUTING = {
    "write code":       "builder",
    "fix bug":          "debugger",
    "debug":            "debugger",
    "design":           "designer",
    "html":             "designer",
    "css":              "designer",
    "plan":             "planner",
    "break down":       "planner",
    "research":         "researcher",
    "test":             "verifier",
    "verify":           "verifier",
    "check":            "verifier",
}


def route_model(task_type: str) -> str:
    return MODEL_ROUTING.get(task_type.lower(), MODEL_ROUTING["default"])


def route_agent(description: str) -> str:
    desc = description.lower()
    for keyword, agent in AGENT_ROUTING.items():
        if keyword in desc:
            return agent
    return "planner"


# ── Behavior tracking ─────────────────────────────────────────────────────────

def record_behavior(event: str, details: dict) -> None:
    entry = {"ts": time.time(), "event": event, **details}
    with _lock:
        with open(BEHAVIOR_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")


def load_behavior(limit: int = 1000) -> list[dict]:
    if not BEHAVIOR_LOG.exists():
        return []
    lines = BEHAVIOR_LOG.read_text(encoding="utf-8").splitlines()
    events = []
    for l in lines[-limit:]:
        try:
            events.append(json.loads(l))
        except Exception:
            pass
    return events


# ── Pattern analysis ──────────────────────────────────────────────────────────

def analyze_patterns() -> dict:
    events = load_behavior()
    if not events:
        return {}

    agent_counts  = defaultdict(int)
    model_counts  = defaultdict(int)
    hourly_counts = defaultdict(int)
    task_durations= []

    start_times = {}
    for e in events:
        if e.get("event") == "task_start":
            start_times[e.get("task_id")] = e["ts"]
            agent_counts[e.get("agent", "unknown")] += 1
            model_counts[e.get("model", "unknown")] += 1
        elif e.get("event") == "task_done":
            tid = e.get("task_id")
            if tid in start_times:
                dur = e["ts"] - start_times.pop(tid)
                task_durations.append(dur)

        hour = int((e["ts"] % 86400) / 3600)
        hourly_counts[hour] += 1

    peak_hour = max(hourly_counts, key=hourly_counts.get) if hourly_counts else None
    avg_dur   = sum(task_durations) / len(task_durations) if task_durations else None

    return {
        "most_used_agent":  max(agent_counts, key=agent_counts.get, default=None),
        "most_used_model":  max(model_counts, key=model_counts.get, default=None),
        "peak_hour":        peak_hour,
        "avg_task_duration_s": round(avg_dur, 1) if avg_dur else None,
        "total_events":     len(events),
        "agent_breakdown":  dict(agent_counts),
    }


def smart_model_select(description: str, system_load: float = 0) -> str:
    """Pick model based on description + current system load."""
    desc = description.lower()

    # Under heavy load, prefer lighter model for non-critical tasks
    if system_load > 85:
        for keyword in ("debug", "fix", "code", "write"):
            if keyword in desc:
                return route_model("code")  # keep heavy model for code
        return MODEL_ROUTING["quick"]

    for keyword in ("code", "debug", "fix", "implement", "function", "class"):
        if keyword in desc:
            return route_model("code")
    for keyword in ("design", "html", "css", "ui", "layout"):
        if keyword in desc:
            return route_model("design")
    for keyword in ("research", "find", "look up", "search"):
        if keyword in desc:
            return route_model("research")

    return route_model("default")


# ── Auto-save analysis periodically ──────────────────────────────────────────

def _analysis_loop() -> None:
    while True:
        time.sleep(3600)  # every hour
        try:
            patterns = analyze_patterns()
            if patterns:
                out = OPT_DIR / "latest_patterns.json"
                out.write_text(json.dumps(patterns, indent=2), encoding="utf-8")
                log.info(f"Pattern analysis saved: {patterns}")
        except Exception as e:
            log.error(f"Optimizer analysis error: {e}")


def start() -> None:
    t = threading.Thread(target=_analysis_loop, daemon=True, name="optimizer")
    t.start()
    log.info("Optimizer started")
