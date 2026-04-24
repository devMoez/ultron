"""Phase 11 — Privacy & User System: per-user profiles, data isolation."""
import json
import threading
import time
from pathlib import Path
from typing import Optional
from core.config import MEMORY_DIR
from core.logger import get_logger

log = get_logger("privacy")

USERS_DIR    = MEMORY_DIR / "personal" / "users"
PROFILES_DIR = MEMORY_DIR / "personal" / "profiles"
USERS_DIR.mkdir(parents=True, exist_ok=True)
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()

# Fields that must never be logged or exported
_SENSITIVE_FIELDS = {"password", "token", "secret", "api_key", "private_key", "ssn", "credit_card"}


# ── User profiles ─────────────────────────────────────────────────────────────

def create_user(username: str, display_name: str = "",
                prefs: Optional[dict] = None) -> dict:
    path = _profile_path(username)
    if path.exists():
        raise ValueError(f"User already exists: {username}")

    profile = {
        "username":     username,
        "display_name": display_name or username,
        "created_at":   time.time(),
        "updated_at":   time.time(),
        "prefs":        prefs or _default_prefs(),
        "data_dir":     str(USERS_DIR / username),
    }
    (USERS_DIR / username).mkdir(parents=True, exist_ok=True)
    _save_profile(username, profile)
    log.info(f"User created: {username}")
    return profile


def get_user(username: str) -> Optional[dict]:
    path = _profile_path(username)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def update_user(username: str, **kwargs) -> bool:
    profile = get_user(username)
    if not profile:
        return False
    for k, v in kwargs.items():
        if k not in _SENSITIVE_FIELDS:
            profile[k] = v
    profile["updated_at"] = time.time()
    _save_profile(username, profile)
    return True


def update_prefs(username: str, prefs: dict) -> bool:
    profile = get_user(username)
    if not profile:
        return False
    profile["prefs"].update(prefs)
    profile["updated_at"] = time.time()
    _save_profile(username, profile)
    return True


def list_users() -> list[str]:
    return [p.stem for p in PROFILES_DIR.glob("*.json")]


def delete_user(username: str, wipe_data: bool = False) -> bool:
    path = _profile_path(username)
    if not path.exists():
        return False
    path.unlink()
    if wipe_data:
        user_dir = USERS_DIR / username
        if user_dir.exists():
            import shutil
            shutil.rmtree(user_dir)
    log.info(f"User deleted: {username}")
    return True


def _profile_path(username: str) -> Path:
    safe = "".join(c for c in username if c.isalnum() or c in "-_")
    return PROFILES_DIR / f"{safe}.json"


def _save_profile(username: str, profile: dict) -> None:
    with _lock:
        _profile_path(username).write_text(
            json.dumps(profile, indent=2, default=str), encoding="utf-8"
        )


def _default_prefs() -> dict:
    return {
        "theme":       "dark",
        "verbosity":   "normal",     # silent | normal | verbose
        "timezone":    "UTC",
        "language":    "en",
        "notify":      True,
        "log_history": True,
        "auto_save":   True,
    }


# ── Per-user data store ───────────────────────────────────────────────────────

def user_write(username: str, key: str, value) -> None:
    user_dir = USERS_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    path = user_dir / f"{key}.json"
    with _lock:
        path.write_text(json.dumps({"key": key, "value": value, "ts": time.time()},
                                   indent=2, default=str), encoding="utf-8")


def user_read(username: str, key: str, default=None):
    path = USERS_DIR / username / f"{key}.json"
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("value", default)
    except Exception:
        return default


# ── .gitignore protection ─────────────────────────────────────────────────────

def ensure_gitignore(root: Path = MEMORY_DIR) -> None:
    """Add sensitive paths to .gitignore."""
    gi = root / ".gitignore"
    patterns = [
        "personal/",
        "shared/state.json",
        "shared/tasks.db",
        "shared/file_tracker/",
        "shared/optimizer/",
        "shared/intelligence/",
        "*.log",
        "*.jsonl",
    ]
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    new_lines = [p for p in patterns if p not in existing]
    if new_lines:
        with open(gi, "a", encoding="utf-8") as f:
            f.write("\n# Ultron — auto-protected\n")
            f.write("\n".join(new_lines) + "\n")
        log.info(f"Updated .gitignore with {len(new_lines)} patterns")


def sanitize(data: dict) -> dict:
    """Remove sensitive fields before logging/exporting."""
    return {k: "***" if k in _SENSITIVE_FIELDS else v for k, v in data.items()}
