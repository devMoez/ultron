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
