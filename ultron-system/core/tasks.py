"""Phase 4 — Task & Reminder system (SQLite-backed)."""
import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Optional
from core.config import MEMORY_DIR
from core.logger import get_logger

log = get_logger("tasks")

DB_PATH = MEMORY_DIR / "shared" / "tasks.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), timeout=10, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    with _connect() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                description TEXT,
                status      TEXT DEFAULT 'pending',
                priority    INTEGER DEFAULT 1,
                progress    INTEGER DEFAULT 0,
                agent       TEXT,
                tags        TEXT DEFAULT '[]',
                created_at  REAL,
                updated_at  REAL,
                due_at      REAL,
                completed_at REAL
            );
            CREATE TABLE IF NOT EXISTS reminders (
                id          TEXT PRIMARY KEY,
                task_id     TEXT,
                message     TEXT NOT NULL,
                remind_at   REAL NOT NULL,
                fired       INTEGER DEFAULT 0,
                created_at  REAL
            );
        """)
    log.info("Task DB initialized")


# ── Tasks ─────────────────────────────────────────────────────────────────────

def create_task(title: str, description: str = "", priority: int = 1,
                agent: str = "", tags: Optional[list] = None,
                due_at: Optional[float] = None) -> str:
    tid = uuid.uuid4().hex[:10]
    now = time.time()
    with _lock:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (tid, title, description, "pending", priority, 0,
                 agent, json.dumps(tags or []), now, now, due_at, None)
            )
    log.info(f"Task created: {tid} — {title}")
    return tid


def update_task(task_id: str, **kwargs) -> bool:
    allowed = {"title", "description", "status", "priority",
               "progress", "agent", "tags", "due_at"}
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if not updates:
        return False
    updates["updated_at"] = time.time()
    if updates.get("status") == "done":
        updates["completed_at"] = time.time()
    if "tags" in updates and isinstance(updates["tags"], list):
        updates["tags"] = json.dumps(updates["tags"])
    cols = ", ".join(f"{k}=?" for k in updates)
    vals = list(updates.values()) + [task_id]
    with _lock:
        with _connect() as conn:
            conn.execute(f"UPDATE tasks SET {cols} WHERE id=?", vals)
    return True


def set_progress(task_id: str, pct: int) -> None:
    update_task(task_id, progress=max(0, min(100, pct)))


def complete_task(task_id: str) -> None:
    update_task(task_id, status="done", progress=100)


def get_task(task_id: str) -> Optional[dict]:
    with _connect() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    return dict(row) if row else None


def list_tasks(status: str = "all", limit: int = 50) -> list[dict]:
    with _connect() as conn:
        if status == "all":
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY priority DESC, created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status=? ORDER BY priority DESC, created_at DESC LIMIT ?",
                (status, limit)
            ).fetchall()
    return [dict(r) for r in rows]


def delete_task(task_id: str) -> None:
    with _lock:
        with _connect() as conn:
            conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
            conn.execute("DELETE FROM reminders WHERE task_id=?", (task_id,))


def stats() -> dict:
    with _connect() as conn:
        total   = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        pending = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='pending'").fetchone()[0]
        done    = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='done'").fetchone()[0]
        failed  = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='failed'").fetchone()[0]
        in_prog = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='in_progress'").fetchone()[0]
    return {"total": total, "pending": pending, "done": done,
            "failed": failed, "in_progress": in_prog}


# ── Reminders ─────────────────────────────────────────────────────────────────

def add_reminder(message: str, remind_at: float,
                 task_id: Optional[str] = None) -> str:
    rid = uuid.uuid4().hex[:10]
    with _lock:
        with _connect() as conn:
            conn.execute(
                "INSERT INTO reminders VALUES (?,?,?,?,?,?)",
                (rid, task_id, message, remind_at, 0, time.time())
            )
    return rid


def due_reminders() -> list[dict]:
    now = time.time()
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM reminders WHERE fired=0 AND remind_at<=?", (now,)
        ).fetchall()
    return [dict(r) for r in rows]


def fire_reminder(reminder_id: str) -> None:
    with _lock:
        with _connect() as conn:
            conn.execute("UPDATE reminders SET fired=1 WHERE id=?", (reminder_id,))


# ── Background reminder watcher ───────────────────────────────────────────────

_reminder_callbacks: list = []

def on_reminder(callback) -> None:
    _reminder_callbacks.append(callback)


def _reminder_loop() -> None:
    while True:
        try:
            for r in due_reminders():
                fire_reminder(r["id"])
                for cb in _reminder_callbacks:
                    try:
                        cb(r)
                    except Exception:
                        pass
                log.info(f"Reminder fired: {r['message']}")
        except Exception as e:
            log.error(f"Reminder loop error: {e}")
        time.sleep(30)


def start_reminder_watcher() -> None:
    t = threading.Thread(target=_reminder_loop, daemon=True, name="reminder-watcher")
    t.start()
    log.info("Reminder watcher started")
