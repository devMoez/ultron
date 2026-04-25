"""Shared configuration for the swarm."""
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent

AGENT_PORTS = {
    "planner":  5005,
    "designer": 5001,
    "builder":  5002,
    "debugger": 5003,
    "verifier": 5004,
}

ORCHESTRATOR_PORT = 5000
ORCHESTRATOR_URL  = f"http://127.0.0.1:{ORCHESTRATOR_PORT}"

DB_PATH        = SWARM_ROOT / "memory" / "shared" / "state.sqlite"
TASKS_QUEUE    = SWARM_ROOT / "tasks" / "queue"
TASKS_PROC     = SWARM_ROOT / "tasks" / "processing"
PROJECTS_DIR   = SWARM_ROOT / "projects"
LOCKS_DIR      = SWARM_ROOT / "locks"
LOGS_DIR       = SWARM_ROOT / "logs"

MAX_RETRIES    = 3
LOCK_STALE_SEC = 30
HEARTBEAT_MISS = 3       # missed heartbeats before restart
POLL_INTERVAL  = 2.0     # seconds between queue polls

# ── Parallel sessions (added 2026-04-25) ──────────────────────────────────────
# Set SWARM_PARALLEL_SESSIONS=1 to enable. Off by default to preserve existing
# single-task semantics. When enabled, the orchestrator's SessionManager owns
# routing (NEW vs EDIT vs CLARIFY) and runs up to MAX_SESSIONS in parallel.
import os as _os

PARALLEL_SESSIONS_ENABLED = _os.environ.get("SWARM_PARALLEL_SESSIONS", "0") == "1"
MAX_SESSIONS              = int(_os.environ.get("SWARM_MAX_SESSIONS", "5"))
MAX_TASKS_PER_AGENT       = int(_os.environ.get("SWARM_MAX_TASKS_PER_AGENT", "5"))

# LLM router config — used by router_llm.py to classify NEW vs EDIT vs CLARIFY
ROUTER_PROVIDER = _os.environ.get("SWARM_ROUTER_PROVIDER", "openrouter")  # openrouter | deepseek | local
ROUTER_MODEL    = _os.environ.get("SWARM_ROUTER_MODEL", "deepseek/deepseek-chat")
ROUTER_API_KEY  = _os.environ.get("OPENROUTER_API_KEY") or _os.environ.get("DEEPSEEK_API_KEY", "")
ROUTER_BASE_URL = _os.environ.get(
    "SWARM_ROUTER_BASE_URL",
    "https://openrouter.ai/api/v1" if _os.environ.get("SWARM_ROUTER_PROVIDER", "openrouter") == "openrouter"
    else "https://api.deepseek.com/v1",
)
ROUTER_TIMEOUT_SEC = float(_os.environ.get("SWARM_ROUTER_TIMEOUT", "8"))

# Agent classification for amend strategy (hybrid mode)
SOFT_INTERRUPT_AGENTS = {"builder", "debugger"}   # poll for amendments mid-task
APPEND_ONLY_AGENTS    = {"planner", "designer", "verifier"}  # read amendment on entry
