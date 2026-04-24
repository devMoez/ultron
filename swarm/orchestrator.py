"""
Step 4: Orchestrator – spawns all agents, watches task queue, manages health.
Run via start.ps1 or: python orchestrator.py
"""
import json
import logging
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI

# Make swarm root importable
SWARM_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SWARM_ROOT))

from swarm_config import (
    AGENT_PORTS, DB_PATH, LOGS_DIR, ORCHESTRATOR_PORT, POLL_INTERVAL,
    TASKS_PROC, TASKS_QUEUE, MAX_RETRIES, HEARTBEAT_MISS, LOCK_STALE_SEC, LOCKS_DIR,
)
from setup_db import init_db, get_connection

# ── Logging ───────────────────────────────────────────────────────────────────
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [orchestrator] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "orchestrator.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("orchestrator")

# ── Agent process tracking ────────────────────────────────────────────────────
agent_processes: dict[str, subprocess.Popen] = {}
agent_last_heartbeat: dict[str, float] = {}
agent_missed: dict[str, int] = {}
agent_retries: dict[str, int] = {}
_lock = threading.Lock()

AGENT_SCRIPTS = {
    name: SWARM_ROOT / "agents" / f"{name}.py"
    for name in AGENT_PORTS
}

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(title="Ultron Swarm Orchestrator")


@app.get("/status")
def status():
    agents = {}
    with _lock:
        for name, proc in agent_processes.items():
            alive = proc.poll() is None
            agents[name] = {
                "port":    AGENT_PORTS[name],
                "alive":   alive,
                "pid":     proc.pid if alive else None,
                "last_hb": agent_last_heartbeat.get(name),
                "missed":  agent_missed.get(name, 0),
                "retries": agent_retries.get(name, 0),
            }
    with get_connection() as conn:
        tasks = [dict(r) for r in conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT 20"
        ).fetchall()]
    return {"agents": agents, "recent_tasks": tasks}


@app.post("/heartbeat")
def heartbeat(payload: dict):
    name = payload.get("agent")
    if not name:
        return {"ok": False}
    with _lock:
        agent_last_heartbeat[name] = time.time()
        agent_missed[name] = 0
    # Update DB
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO agents(name,status,last_heartbeat,port,pid) VALUES(?,?,?,?,?) "
                "ON CONFLICT(name) DO UPDATE SET status=excluded.status, "
                "last_heartbeat=excluded.last_heartbeat, port=excluded.port, pid=excluded.pid",
                (name, payload.get("status", "idle"), time.time(),
                 payload.get("port"), payload.get("pid")),
            )
    except Exception as e:
        log.warning(f"DB heartbeat update failed: {e}")
    return {"ok": True}


@app.post("/task_result")
def task_result(payload: dict):
    task_id = payload.get("task_id")
    success  = payload.get("success", False)
    result   = payload.get("result", "")
    agent    = payload.get("agent", "")
    log.info(f"Task {task_id} completed by {agent}: success={success}")
    if task_id is None:
        return {"ok": False}
    try:
        with get_connection() as conn:
            conn.execute(
                "UPDATE tasks SET status=?, completed_at=?, result=? WHERE id=?",
                ("done" if success else "failed", time.time(), result, task_id),
            )
            if not success:
                row = conn.execute(
                    "SELECT retry_count, project_path, assigned_agent FROM tasks WHERE id=?",
                    (task_id,),
                ).fetchone()
                if row and row["retry_count"] < MAX_RETRIES:
                    conn.execute(
                        "UPDATE tasks SET status='queued', retry_count=retry_count+1 WHERE id=?",
                        (task_id,),
                    )
                    log.info(f"Re-queued task {task_id} (retry {row['retry_count']+1})")
                elif row:
                    log.error(f"Task {task_id} exhausted retries – attempting rollback")
                    _git_rollback(row["project_path"])
    except Exception as e:
        log.error(f"task_result DB error: {e}")
    return {"ok": True}


# ── Git rollback ──────────────────────────────────────────────────────────────

def _git_rollback(project_path: str | None) -> None:
    if not project_path:
        log.warning("No project_path for rollback – skipping")
        return
    p = Path(project_path)
    if not (p / ".git").exists():
        log.warning(f"{project_path} is not a git repo – skipping rollback")
        return
    try:
        subprocess.run(["git", "restore", "."], cwd=str(p), check=True)
        log.info(f"Git restore completed in {project_path}")
    except subprocess.CalledProcessError as e:
        log.error(f"Git restore failed: {e}")


# ── Spawn agents ──────────────────────────────────────────────────────────────

def _spawn_agent(name: str) -> subprocess.Popen:
    script = AGENT_SCRIPTS[name]
    log_file = open(LOGS_DIR / f"{name}.log", "a", encoding="utf-8")
    env = {**os.environ, "ORCHESTRATOR_URL": f"http://127.0.0.1:{ORCHESTRATOR_PORT}"}
    proc = subprocess.Popen(
        [sys.executable, str(script)],
        stdout=log_file,
        stderr=log_file,
        env=env,
        cwd=str(SWARM_ROOT),
    )
    log.info(f"Spawned {name} (pid={proc.pid})")
    return proc


def _start_all_agents() -> None:
    for name in AGENT_PORTS:
        with _lock:
            agent_retries[name] = 0
            agent_missed[name]  = 0
        proc = _spawn_agent(name)
        with _lock:
            agent_processes[name] = proc


# ── Health monitor ────────────────────────────────────────────────────────────

def _health_monitor() -> None:
    interval = 5.0
    while True:
        time.sleep(interval)
        now = time.time()
        # Check stale locks
        for lf in LOCKS_DIR.glob("*.lock"):
            try:
                if now - lf.stat().st_mtime > LOCK_STALE_SEC:
                    log.warning(f"Stale lock {lf.name} – removing")
                    lf.unlink(missing_ok=True)
            except Exception:
                pass
        # Check agent heartbeats
        with _lock:
            names = list(agent_processes.keys())
        for name in names:
            with _lock:
                last = agent_last_heartbeat.get(name, 0)
                proc = agent_processes.get(name)
            if proc and proc.poll() is not None:
                log.warning(f"{name} process died – restarting")
                _restart_agent(name)
                continue
            if last and (now - last) > (HEARTBEAT_MISS * 5 + 2):
                with _lock:
                    agent_missed[name] = agent_missed.get(name, 0) + 1
                    missed = agent_missed[name]
                if missed >= HEARTBEAT_MISS:
                    log.warning(f"{name} missed {missed} heartbeats – restarting")
                    _restart_agent(name)


def _restart_agent(name: str) -> None:
    with _lock:
        retries = agent_retries.get(name, 0)
        if retries >= MAX_RETRIES:
            log.error(f"{name} exceeded max restarts ({MAX_RETRIES}) – not restarting")
            return
        proc = agent_processes.get(name)
    if proc:
        try:
            proc.kill()
        except Exception:
            pass
    time.sleep(1)
    new_proc = _spawn_agent(name)
    with _lock:
        agent_processes[name] = new_proc
        agent_retries[name]   = retries + 1
        agent_missed[name]    = 0
        agent_last_heartbeat.pop(name, None)


# ── Task queue watcher ────────────────────────────────────────────────────────

def _dispatch_task(task_file: Path) -> None:
    try:
        data = json.loads(task_file.read_text(encoding="utf-8"))
    except Exception as e:
        log.error(f"Bad task file {task_file.name}: {e}")
        task_file.unlink(missing_ok=True)
        return

    agent = data.get("target_agent", "planner")
    desc  = data.get("description", "")
    proj  = data.get("project_path", "")

    # Move to processing
    dest = TASKS_PROC / task_file.name
    shutil.move(str(task_file), str(dest))

    # Insert into DB
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO tasks(description,assigned_agent,status,created_at,project_path,source_file) "
                "VALUES(?,?,?,?,?,?)",
                (desc, agent, "queued", time.time(), proj, str(dest)),
            )
            task_id = cur.lastrowid
    except Exception as e:
        log.error(f"DB insert failed: {e}")
        return

    log.info(f"Dispatching task {task_id} → {agent}: {desc[:60]}")

    port = AGENT_PORTS.get(agent)
    if not port:
        log.error(f"Unknown agent '{agent}' in task {task_file.name}")
        return

    try:
        resp = httpx.post(
            f"http://127.0.0.1:{port}/assign_task",
            json={**data, "id": task_id},
            timeout=5.0,
        )
        if resp.status_code == 200:
            with get_connection() as conn:
                conn.execute(
                    "UPDATE tasks SET status='assigned', started_at=? WHERE id=?",
                    (time.time(), task_id),
                )
        else:
            log.warning(f"Agent {agent} rejected task: {resp.text}")
    except Exception as e:
        log.warning(f"Could not reach {agent} for task {task_id}: {e}")


def _queue_watcher() -> None:
    TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
    TASKS_PROC.mkdir(parents=True, exist_ok=True)
    while True:
        for jf in sorted(TASKS_QUEUE.glob("*.json")):
            _dispatch_task(jf)
        time.sleep(POLL_INTERVAL)


# ── Entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info("Initializing database...")
    init_db()

    log.info("Starting all agents...")
    _start_all_agents()
    time.sleep(2)  # give agents a moment to boot

    log.info("Starting health monitor...")
    threading.Thread(target=_health_monitor, daemon=True, name="health").start()

    log.info("Starting task queue watcher...")
    threading.Thread(target=_queue_watcher, daemon=True, name="queue").start()

    log.info(f"Orchestrator listening on port {ORCHESTRATOR_PORT}")
    uvicorn.run(app, host="127.0.0.1", port=ORCHESTRATOR_PORT, log_level="warning")
