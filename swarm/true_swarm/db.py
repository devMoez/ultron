import sqlite3
import os
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent
DB_PATH = SWARM_ROOT / "memory" / "swarm_state.sqlite"

def get_connection(timeout: float = 5.0):
    conn = sqlite3.connect(DB_PATH, timeout=timeout)
    conn.row_factory = sqlite3.Row
    # Enable WAL for better concurrency
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_connection() as conn:
        conn.executescript("""
            -- Agents table: tracks each agent's state
            CREATE TABLE IF NOT EXISTS agents (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT    NOT NULL UNIQUE,
                status          TEXT    NOT NULL DEFAULT 'offline',  -- offline, idle, busy, retired
                last_heartbeat  REAL,
                port            INTEGER,
                pid             INTEGER,
                skills          TEXT,  -- JSON list of skill names
                success_rate    REAL   DEFAULT 0.0,  -- running average of success
                tasks_completed INTEGER DEFAULT 0,
                created_at      REAL   NOT NULL
            );

            -- Tasks table: tasks posted to the blackboard
            CREATE TABLE IF NOT EXISTS tasks (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                description     TEXT    NOT NULL,
                required_skills TEXT,  -- JSON list of skill names
                priority        INTEGER DEFAULT 0,
                status          TEXT    NOT NULL DEFAULT 'queued',  -- queued, claimed, done, failed
                assigned_agent  INTEGER,  -- foreign key to agents.id
                claimed_at      REAL,
                completed_at    REAL,
                result          TEXT,
                retry_count     INTEGER NOT NULL DEFAULT 0,
                project_path    TEXT,
                created_at      REAL   NOT NULL
            );

            -- Skill library: stores skill implementations and metadata
            CREATE TABLE IF NOT EXISTS skills (
                name            TEXT    NOT NULL,
                version         TEXT    NOT NULL,
                source          TEXT    NOT NULL,  -- the code or path to the module
                metadata        TEXT,  -- JSON: input_types, output_types, resource_reqs, etc.
                PRIMARY KEY (name, version)
            );

            -- Episodic memory: per-agent log of actions and observations
            CREATE TABLE IF NOT EXISTS episodic_memory (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id        INTEGER NOT NULL REFERENCES agents(id),
                timestamp       REAL    NOT NULL,
                event_type      TEXT    NOT NULL,  -- e.g., 'task_start', 'task_end', 'observation'
                data            TEXT,  -- JSON blob
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            );

            -- Semantic memory: shared facts, learned patterns, skill weights
            CREATE TABLE IF NOT EXISTS semantic_memory (
                key             TEXT    NOT NULL,
                value           TEXT    NOT NULL,  -- JSON
                updated_at      REAL    NOT NULL,
                PRIMARY KEY (key)
            );

            -- Indexes for performance
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
            CREATE INDEX IF NOT EXISTS idx_episodic_agent ON episodic_memory(agent_id);
        """)
    print(f"[db] Database initialized at {DB_PATH}")