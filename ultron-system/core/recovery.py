"""Phase 7 — Auto Recovery: crash detection, task resume, watchdog."""
import json
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, Callable
from core.config import ROOT, MEMORY_DIR
from core.logger import get_logger
from core import state, tasks as task_mgr

log = get_logger("recovery")

RECOVERY_LOG = MEMORY_DIR / "shared" / "recovery.jsonl"
RECOVERY_LOG.parent.mkdir(parents=True, exist_ok=True)

_notify_handlers: list[Callable] = []
_watchdog_targets: dict[str, dict] = {}  # name → {cmd, restart_fn, failures, max_failures}
_lock = threading.Lock()


# ── Notification ──────────────────────────────────────────────────────────────

def on_notify(callback: Callable) -> None:
    """Register a callback for crash/recovery events."""
    _notify_handlers.append(callback)


def _notify(event: str, details: dict) -> None:
    entry = {"ts": time.time(), "event": event, **details}
    with open(RECOVERY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    log.warning(f"[RECOVERY] {event}: {details}")
    for cb in _notify_handlers:
        try:
            cb(entry)
        except Exception:
            pass


# ── Task resume ───────────────────────────────────────────────────────────────

def mark_in_progress(task_id: str, checkpoint: Optional[dict] = None) -> None:
    """Record that a task is running (for resume on restart)."""
    task_mgr.update_task(task_id, status="in_progress")
    if checkpoint:
        state.set(f"checkpoint_{task_id}", checkpoint)


def save_checkpoint(task_id: str, data: dict) -> None:
    state.set(f"checkpoint_{task_id}", {"ts": time.time(), "data": data})


def load_checkpoint(task_id: str) -> Optional[dict]:
    return state.get(f"checkpoint_{task_id}")


def resume_interrupted_tasks() -> list[str]:
    """Find tasks that were in_progress at last shutdown and re-queue them."""
    interrupted = task_mgr.list_tasks(status="in_progress")
    resumed = []
    for t in interrupted:
        task_mgr.update_task(t["id"], status="pending", progress=0)
        _notify("task_resumed", {"task_id": t["id"], "title": t["title"]})
        resumed.append(t["id"])
        log.info(f"Resumed interrupted task: {t['id']}")
    return resumed


# ── Watchdog ──────────────────────────────────────────────────────────────────

def register_watchdog(name: str, check_fn: Callable[[], bool],
                       restart_fn: Callable[[], None],
                       max_failures: int = 3) -> None:
    """Register a service to be watched. check_fn returns True if alive."""
    with _lock:
        _watchdog_targets[name] = {
            "check_fn":    check_fn,
            "restart_fn":  restart_fn,
            "failures":    0,
            "max_failures":max_failures,
            "last_ok":     time.time(),
        }
    log.info(f"Watchdog registered: {name}")


def _watchdog_loop() -> None:
    while True:
        time.sleep(15)
        with _lock:
            targets = dict(_watchdog_targets)
        for name, info in targets.items():
            try:
                alive = info["check_fn"]()
            except Exception as e:
                alive = False
                log.error(f"Watchdog check error for {name}: {e}")

            if alive:
                with _lock:
                    if name in _watchdog_targets:
                        _watchdog_targets[name]["failures"] = 0
                        _watchdog_targets[name]["last_ok"] = time.time()
            else:
                with _lock:
                    if name in _watchdog_targets:
                        _watchdog_targets[name]["failures"] += 1
                        failures = _watchdog_targets[name]["failures"]
                        max_f    = _watchdog_targets[name]["max_failures"]

                log.warning(f"Watchdog: {name} down (failure {failures}/{max_f})")
                _notify("service_down", {"name": name, "failures": failures})

                if failures <= max_f:
                    try:
                        info["restart_fn"]()
                        _notify("service_restarted", {"name": name})
                        log.info(f"Restarted: {name}")
                    except Exception as e:
                        log.error(f"Restart failed for {name}: {e}")
                else:
                    _notify("service_dead", {"name": name, "msg": "max failures exceeded"})


def start_watchdog() -> None:
    t = threading.Thread(target=_watchdog_loop, daemon=True, name="watchdog")
    t.start()
    log.info("Watchdog started")


# ── Crash log reader ──────────────────────────────────────────────────────────

def recent_crashes(n: int = 20) -> list[dict]:
    if not RECOVERY_LOG.exists():
        return []
    try:
        lines = RECOVERY_LOG.read_text(encoding="utf-8").splitlines()
        events = [json.loads(l) for l in lines[-n:] if l.strip()]
        return [e for e in events if e.get("event") in
                ("service_down", "service_dead", "task_resumed")]
    except Exception:
        return []
