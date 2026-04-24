"""Phase 1 — Configuration manager."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SWARM_URL = os.environ.get("SWARM_URL", "http://127.0.0.1:5000")
DASHBOARD_PORT = int(os.environ.get("DASHBOARD_PORT", "5010"))

LOGS_DIR   = ROOT / "logs"
MEMORY_DIR = ROOT / "memory"

LOGS_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
