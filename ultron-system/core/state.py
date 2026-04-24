"""Phase 1 — System state manager."""
import json
import time
import threading
from pathlib import Path
from core.config import MEMORY_DIR

STATE_FILE = MEMORY_DIR / "shared" / "state.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()
_state: dict = {
    "active_agents": {},
    "running_tasks": {},
    "resource_snapshot": {},
    "started_at": time.time(),
}

def load() -> None:
    global _state
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                _state.update(json.load(f))
        except Exception:
            pass

def save() -> None:
    with _lock:
        STATE_FILE.write_text(json.dumps(_state, indent=2), encoding="utf-8")

def get(key: str, default=None):
    with _lock:
        return _state.get(key, default)

def set(key: str, value) -> None:
    with _lock:
        _state[key] = value
    save()

def all() -> dict:
    with _lock:
        return dict(_state)
