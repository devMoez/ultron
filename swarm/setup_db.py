"""
Step 2: SQLite schema setup for the Ultron swarm shared state.
Run once to initialize: python setup_db.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "memory", "shared", "state.sqlite")


def get_connection(timeout: float = 5.0) -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=timeout)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS agents (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT    NOT NULL UNIQUE,
                status          TEXT    NOT NULL DEFAULT 'offline',
                last_heartbeat  REAL,
                port            INTEGER,
                pid             INTEGER,
                current_task_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                description     TEXT    NOT NULL,
                assigned_agent  TEXT    NOT NULL,
                status          TEXT    NOT NULL DEFAULT 'queued',
                created_at      REAL    NOT NULL,
                started_at      REAL,
                completed_at    REAL,
                result          TEXT,
                retry_count     INTEGER NOT NULL DEFAULT 0,
                project_path    TEXT,
                source_file     TEXT
            );

            CREATE TABLE IF NOT EXISTS artifacts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id     INTEGER NOT NULL REFERENCES tasks(id),
                file_path   TEXT    NOT NULL,
                hash        TEXT
            );

            CREATE TABLE IF NOT EXISTS locks (
                file_path   TEXT PRIMARY KEY,
                agent_name  TEXT NOT NULL,
                acquired_at REAL NOT NULL
            );
        """)
    print(f"[setup_db] Database initialized at {DB_PATH}")


if __name__ == "__main__":
    init_db()
