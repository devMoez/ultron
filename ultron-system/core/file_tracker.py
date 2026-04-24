"""Phase 6 — File Tracker: git-style snapshots, change history, rollback."""
import hashlib
import json
import shutil
import time
import threading
from pathlib import Path
from typing import Optional
from core.config import MEMORY_DIR
from core.logger import get_logger

log = get_logger("file_tracker")

TRACK_DIR = MEMORY_DIR / "shared" / "file_tracker"
SNAPSHOTS = TRACK_DIR / "snapshots"
HISTORY   = TRACK_DIR / "history.jsonl"

TRACK_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOTS.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


# ── Hashing ───────────────────────────────────────────────────────────────────

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except Exception:
        return ""
    return h.hexdigest()[:16]


# ── Snapshot ──────────────────────────────────────────────────────────────────

def snapshot(path: str, label: str = "") -> str:
    """Save a snapshot of a file. Returns snapshot ID."""
    src = Path(path)
    if not src.exists():
        raise FileNotFoundError(path)

    snap_id = f"{int(time.time())}_{_hash_file(src)}"
    snap_dir = SNAPSHOTS / src.name
    snap_dir.mkdir(parents=True, exist_ok=True)
    dst = snap_dir / snap_id

    shutil.copy2(src, dst)

    entry = {
        "id":       snap_id,
        "path":     str(path),
        "label":    label,
        "hash":     _hash_file(src),
        "size":     src.stat().st_size,
        "ts":       time.time(),
        "snapshot": str(dst),
    }
    with _lock:
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    log.info(f"Snapshot {snap_id} for {path}")
    return snap_id


def rollback(path: str, snap_id: str) -> bool:
    """Restore a file from a snapshot."""
    src_path = Path(path)
    entries = _history_for(path)
    for e in entries:
        if e["id"] == snap_id:
            snap_file = Path(e["snapshot"])
            if snap_file.exists():
                shutil.copy2(snap_file, src_path)
                log.info(f"Rolled back {path} to {snap_id}")
                _record_event("rollback", path, {"snap_id": snap_id})
                return True
    log.error(f"Snapshot {snap_id} not found for {path}")
    return False


def _history_for(path: str) -> list[dict]:
    if not HISTORY.exists():
        return []
    results = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(line)
            if e.get("path") == str(path):
                results.append(e)
        except Exception:
            pass
    return sorted(results, key=lambda x: x["ts"], reverse=True)


def history(path: str, limit: int = 20) -> list[dict]:
    return _history_for(path)[:limit]


def list_snapshots(path: str) -> list[str]:
    return [e["id"] for e in _history_for(path)]


# ── Change detection ──────────────────────────────────────────────────────────

_watched: dict[str, str] = {}  # path → last known hash
_watch_lock = threading.Lock()
_change_callbacks: list = []


def watch(path: str) -> None:
    p = Path(path)
    if p.exists():
        with _watch_lock:
            _watched[path] = _hash_file(p)


def unwatch(path: str) -> None:
    with _watch_lock:
        _watched.pop(path, None)


def on_change(callback) -> None:
    _change_callbacks.append(callback)


def _scan_watched() -> None:
    with _watch_lock:
        items = list(_watched.items())
    for path, old_hash in items:
        p = Path(path)
        new_hash = _hash_file(p) if p.exists() else ""
        if new_hash != old_hash:
            with _watch_lock:
                _watched[path] = new_hash
            event = {"path": path, "old_hash": old_hash, "new_hash": new_hash, "ts": time.time()}
            log.info(f"Change detected: {path}")
            _record_event("change", path, {"old": old_hash, "new": new_hash})
            for cb in _change_callbacks:
                try:
                    cb(event)
                except Exception:
                    pass


def _record_event(event_type: str, path: str, details: dict) -> None:
    entry = {"event": event_type, "path": path, "ts": time.time(), **details}
    with _lock:
        with open(HISTORY, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")


# ── Watcher thread ────────────────────────────────────────────────────────────

_watching = False

def start_watcher(interval: int = 10) -> None:
    global _watching
    if _watching:
        return
    _watching = True

    def _loop():
        while _watching:
            try:
                _scan_watched()
            except Exception as e:
                log.error(f"File watcher error: {e}")
            time.sleep(interval)

    t = threading.Thread(target=_loop, daemon=True, name="file-watcher")
    t.start()
    log.info("File watcher started")
