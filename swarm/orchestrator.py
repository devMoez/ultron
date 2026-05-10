"""
This file handles the primary Python orchestration for multi-agent swarm tasks.
Step 4: Orchestrator – spawns all agents, watches task queue, manages health.
Enhanced with: WebSocket real-time push, DAG, AgentRegistry, MessageBus, SkillOrchestra.
Run via start.ps1 or: python orchestrator.py
"""
import asyncio
import json
import logging
import os
import shutil
import subprocess
import sys
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Set

import httpx
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Make swarm root importable
SWARM_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SWARM_ROOT))

# Always use the swarm venv Python to spawn agents (avoids sys.executable
# resolving to a different venv when the user runs `python orchestrator.py`).
_VENV_PYTHON = SWARM_ROOT / "venv" / "Scripts" / "python.exe"
AGENT_PYTHON = str(_VENV_PYTHON) if _VENV_PYTHON.exists() else sys.executable

from swarm_config import (
    AGENT_PORTS, DB_PATH, LOGS_DIR, ORCHESTRATOR_PORT, POLL_INTERVAL,
    TASKS_PROC, TASKS_QUEUE, MAX_RETRIES, HEARTBEAT_MISS, LOCK_STALE_SEC, LOCKS_DIR,
    PARALLEL_SESSIONS_ENABLED, MAX_SESSIONS,
)
from setup_db import init_db, get_connection
# Session manager is optional — only loaded when parallel sessions are enabled.
session_manager = None  # type: ignore[assignment]
if PARALLEL_SESSIONS_ENABLED:
    from session_manager import SessionManager
    session_manager = SessionManager(max_sessions=MAX_SESSIONS)

# ── Swarm Core (new modules — safe to import, no side effects) ────────────────
try:
    from core.dag import shared_dag
    from core.agent_registry import shared_registry
    from core.message_bus import shared_bus
    from core.skill_orchestra import SkillOrchestra
    _CORE_LOADED = True
except Exception as _e:
    log_boot = logging.getLogger("orchestrator")
    log_boot.warning(f"Swarm core modules not loaded: {_e}")
    shared_dag = None  # type: ignore
    shared_registry = None  # type: ignore
    shared_bus = None  # type: ignore
    SkillOrchestra = None  # type: ignore
    _CORE_LOADED = False

# ── Logging ───────────────────────────────────────────────────────────────────
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [orchestrator] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "orchestrator.log", encoding="utf-8"),
        logging.StreamHandler(sys.stderr),
    ],
)
log = logging.getLogger("orchestrator")

# ── Agent skill map (used by registry auto-register on heartbeat) ─────────────
_AGENT_SKILLS: dict[str, list[str]] = {
    "planner":  ["plan", "decompose"],
    "designer": ["design", "ui", "css"],
    "builder":  ["code", "build", "spawn_agent"],
    "debugger": ["debug", "test"],
    "verifier": ["verify", "test"],
}

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

# ── FastAPI app with lifespan (handles startup even when run via uvicorn orchestrator:app) ──

_startup_done = False
_startup_lock = threading.Lock()

def _startup() -> None:
    """Initialize DB, spawn agents, start background threads (idempotent)."""
    global _startup_done
    with _startup_lock:
        if _startup_done:
            log.info("Startup already done, skipping")
            return
        _startup_done = True

    log.info("Initializing database...")
    init_db()

    log.info("Starting all agents...")
    _start_all_agents()
    time.sleep(2)

    # Pre-register known agents
    if shared_registry and _CORE_LOADED:
        for aname, aport in AGENT_PORTS.items():
            shared_registry.register(aname, _AGENT_SKILLS.get(aname, []), aport)
        log.info("Agent registry populated")

    # Start SkillOrchestra
    if _CORE_LOADED and SkillOrchestra:
        def _spawn_skill(skill: str):
            import uuid as _uuid
            name = f"{skill}_agent_{_uuid.uuid4().hex[:4]}"
            shared_registry.register(name, [skill], port=0, spawned=True)
            log.info(f"SkillOrchestra spawned virtual agent {name!r} for skill {skill!r}")

        orchestra = SkillOrchestra(
            dag=shared_dag,
            registry=shared_registry,
            bus=shared_bus,
            spawn_skill_fn=_spawn_skill,
            poll_interval=2.0,
        )
        orchestra.start()
        log.info("SkillOrchestra started")

    log.info("Starting health monitor...")
    threading.Thread(target=_health_monitor, daemon=True, name="health").start()

    log.info("Starting task queue watcher...")
    threading.Thread(target=_queue_watcher, daemon=True, name="queue").start()

    log.info("Swarm orchestrator fully initialized")


@asynccontextmanager
async def _lifespan(app: FastAPI):
    """FastAPI lifespan: runs startup on ASGI serve, cleans up on shutdown."""
    log.info("Lifespan startup — running initialization...")
    _startup()
    log.info(f"Orchestrator ready on port {ORCHESTRATOR_PORT}")
    yield
    log.info("Lifespan shutdown — cleaning up...")
    # Optionally stop agent processes
    with _lock:
        for name, proc in agent_processes.items():
            if proc.poll() is None:
                proc.terminate()
                log.info(f"Agent {name} terminated")


app = FastAPI(title="Ultron Swarm Orchestrator", lifespan=_lifespan)

# Allow the Ultron web UI (any localhost port) to poll the orchestrator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve Swarm UI (single-page app from swarm/ui/) ───────────────────────
_UI_DIR = SWARM_ROOT / "ui"
if _UI_DIR.exists():
    # Mount static assets (css, js, etc.) under /static/
    app.mount("/static", StaticFiles(directory=str(_UI_DIR)), name="ui-static")

    @app.get("/")
    def serve_ui():
        return FileResponse(_UI_DIR / "index.html")

    log.info(f"Serving UI from {_UI_DIR} at /")
else:
    log.warning(f"No UI directory found at {_UI_DIR}")

# ── WebSocket connection manager ──────────────────────────────────────────────
class _WSManager:
    def __init__(self):
        self._clients: Set[WebSocket] = set()
        self._lock = threading.Lock()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        with self._lock:
            self._clients.add(ws)

    def disconnect(self, ws: WebSocket):
        with self._lock:
            self._clients.discard(ws)

    def broadcast_sync(self, data: dict):
        """Call from non-async thread to push update to all WS clients."""
        payload = json.dumps(data)
        dead = []
        with self._lock:
            clients = list(self._clients)
        for ws in clients:
            try:
                loop = ws.send_text.__self__._loop  # type: ignore
                asyncio.run_coroutine_threadsafe(ws.send_text(payload), loop)
            except Exception:
                dead.append(ws)
        for d in dead:
            self.disconnect(d)

ws_manager = _WSManager()
_ws_loop: asyncio.AbstractEventLoop | None = None   # set when uvicorn starts


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
    sessions_summary = None
    if session_manager is not None:
        all_sess = session_manager.list_sessions()
        sessions_summary = {
            "total":     len(all_sess),
            "active":    sum(1 for s in all_sess if s["status"] == "active"),
            "queued":    sum(1 for s in all_sess if s["status"] == "queued"),
            "done":      sum(1 for s in all_sess if s["status"] == "done"),
            "failed":    sum(1 for s in all_sess if s["status"] == "failed"),
            "max":       MAX_SESSIONS,
            "sessions":  all_sess,
        }
    return {"agents": agents, "recent_tasks": tasks, "sessions": sessions_summary,
            "parallel_enabled": PARALLEL_SESSIONS_ENABLED}


@app.post("/submit")
def submit_task(payload: dict):
    """Submit a task from the UI: {description, target_agent?, project_path?}"""
    description = (payload or {}).get("description", "").strip()
    if not description:
        return {"ok": False, "error": "description is required"}
    target_agent = payload.get("target_agent", "planner")
    project_path = payload.get("project_path", "")
    # Write to task queue as a JSON file
    import uuid, time as _time
    task_id = str(uuid.uuid4())[:8]
    task_file = TASKS_QUEUE / f"{_time.time():.6f}_{task_id}.json"
    TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
    task_file.write_text(
        json.dumps({"description": description, "target_agent": target_agent, "project_path": project_path}),
        encoding="utf-8",
    )
    log.info(f"UI submitted task [{task_id}] → {target_agent}: {description[:60]}")
    return {"ok": True, "task_id": task_id}


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
    # Update shared registry
    if shared_registry and _CORE_LOADED:
        # Register if not already known (happens when orchestrator restarts)
        if not shared_registry.get(name):
            from swarm_config import AGENT_PORTS as _AP
            port = payload.get("port") or _AP.get(name, 0)
            shared_registry.register(name, _AGENT_SKILLS.get(name, []), port)
        shared_registry.heartbeat(
            name,
            status=payload.get("status", "idle"),
            pid=payload.get("pid"),
        )
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
    # Notify SessionManager so it can update / promote queued sessions.
    if session_manager is not None:
        try:
            session_manager.mark_session_done(int(task_id), success, str(result))
        except Exception as e:
            log.warning(f"session_manager.mark_session_done failed: {e}")
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


# ── WebSocket real-time push ──────────────────────────────────────────────────

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    global _ws_loop
    _ws_loop = asyncio.get_event_loop()
    await ws_manager.connect(ws)
    try:
        # Send initial snapshot
        await ws.send_text(json.dumps({"type": "init", "data": _build_snapshot()}))
        while True:
            # Keep alive — client pings with "ping"
            msg = await ws.receive_text()
            if msg == "ping":
                await ws.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)


def _build_snapshot() -> dict:
    """Full status snapshot for initial WS push or polling."""
    agents_proc = {}
    with _lock:
        for name, proc in agent_processes.items():
            alive = proc.poll() is None
            agents_proc[name] = {
                "port":    AGENT_PORTS[name],
                "alive":   alive,
                "pid":     proc.pid if alive else None,
                "last_hb": agent_last_heartbeat.get(name),
                "missed":  agent_missed.get(name, 0),
                "retries": agent_retries.get(name, 0),
            }
    # Merge registry info (skills, status)
    if shared_registry and _CORE_LOADED:
        for reg_agent in shared_registry.all_agents():
            n = reg_agent["name"]
            if n in agents_proc:
                agents_proc[n].update({
                    "skills": reg_agent["skills"],
                    "status": reg_agent["status"],
                    "current_task": reg_agent["current_task"],
                    "spawned": reg_agent["spawned"],
                })
            else:
                agents_proc[n] = reg_agent
    with get_connection() as conn:
        tasks = [dict(r) for r in conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT 40"
        ).fetchall()]
    dag_nodes = shared_dag.get_all() if shared_dag else []
    dag_edges = shared_dag.get_edges() if shared_dag else []
    bus_log   = shared_bus.get_log() if shared_bus else []
    return {
        "agents":    agents_proc,
        "tasks":     tasks,
        "dag":       {"nodes": dag_nodes, "edges": dag_edges},
        "bus_log":   bus_log[-50:],
    }


def _push_update(event_type: str, data: dict):
    """Push incremental update to all WS clients (call from any thread)."""
    if not _ws_loop:
        return
    payload = json.dumps({"type": event_type, **data})
    with ws_manager._lock:
        clients = list(ws_manager._clients)
    for ws in clients:
        try:
            asyncio.run_coroutine_threadsafe(ws.send_text(payload), _ws_loop)
        except Exception:
            pass


# ── Agent control (spawn / kill / pause / resume / assign) ───────────────────

@app.post("/agents/spawn")
def spawn_agent_endpoint(payload: dict):
    """Spawn a new agent process. Body: {name?, skills: [str], port?}"""
    skills = (payload or {}).get("skills", [])
    name   = (payload or {}).get("name", f"agent_{int(time.time())}")
    if not skills:
        return {"ok": False, "error": "skills list required"}
    if shared_registry and _CORE_LOADED:
        shared_registry.register(name, skills, port=0, spawned=True)
    _push_update("agent_spawned", {"name": name, "skills": skills})
    log.info(f"UI spawned agent: {name!r} skills={skills}")
    return {"ok": True, "name": name, "skills": skills}


@app.post("/agents/{name}/kill")
def kill_agent(name: str):
    """Kill (terminate) a running agent process."""
    with _lock:
        proc = agent_processes.get(name)
    if not proc:
        return {"ok": False, "error": f"Agent {name!r} not found"}
    try:
        proc.kill()
    except Exception as e:
        return {"ok": False, "error": str(e)}
    if shared_registry and _CORE_LOADED:
        shared_registry.unregister(name)
    _push_update("agent_killed", {"name": name})
    log.info(f"Agent {name!r} killed by UI")
    return {"ok": True}


@app.post("/agents/{name}/pause")
def pause_agent(name: str):
    if shared_registry and _CORE_LOADED:
        ok = shared_registry.pause(name)
        _push_update("agent_paused", {"name": name})
        return {"ok": ok}
    return {"ok": False, "error": "registry not loaded"}


@app.post("/agents/{name}/resume")
def resume_agent(name: str):
    if shared_registry and _CORE_LOADED:
        ok = shared_registry.resume(name)
        _push_update("agent_resumed", {"name": name})
        return {"ok": ok}
    return {"ok": False, "error": "registry not loaded"}


@app.post("/agents/{name}/assign")
def assign_task_to_agent(name: str, payload: dict):
    """Manually assign a task to a specific agent, bypassing skill routing."""
    description = (payload or {}).get("description", "").strip()
    if not description:
        return {"ok": False, "error": "description required"}
    import uuid as _uuid, time as _t
    task_id = _uuid.uuid4().hex[:8]
    task_file = TASKS_QUEUE / f"{_t.time():.6f}_{task_id}.json"
    TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
    task_file.write_text(json.dumps({
        "description": description,
        "target_agent": name,
        "project_path": payload.get("project_path", ""),
    }), encoding="utf-8")
    log.info(f"UI manually assigned task [{task_id}] to {name!r}: {description[:60]}")
    return {"ok": True, "task_id": task_id}


# ── DAG endpoints ─────────────────────────────────────────────────────────────

@app.get("/dag")
def get_dag():
    if not shared_dag or not _CORE_LOADED:
        return {"ok": False, "error": "DAG not loaded"}
    return {
        "ok":    True,
        "nodes": shared_dag.get_all(),
        "edges": shared_dag.get_edges(),
    }


@app.post("/dag/submit")
def submit_dag_task(payload: dict):
    """Add a task directly to the DAG (skill-routed). Body: {description, skills: [str]}"""
    if not shared_dag or not _CORE_LOADED:
        return {"ok": False, "error": "DAG not loaded"}
    desc   = (payload or {}).get("description", "").strip()
    skills = (payload or {}).get("skills", ["plan"])
    if not desc:
        return {"ok": False, "error": "description required"}
    task = shared_dag.add_task(desc, skills)
    _push_update("dag_task_added", {"task": task.to_dict()})
    return {"ok": True, "task_id": task.id}


@app.get("/dag/events")
def dag_events(since: float = 0.0):
    if not shared_dag or not _CORE_LOADED:
        return {"events": []}
    return {"events": shared_dag.get_events(since)}


# ── Bus log ───────────────────────────────────────────────────────────────────

@app.get("/bus/log")
def bus_log(since: float = 0.0, limit: int = 100):
    if not shared_bus or not _CORE_LOADED:
        return {"log": []}
    return {"log": shared_bus.get_log(since=since, limit=limit)}


# ── Registry ──────────────────────────────────────────────────────────────────

@app.get("/registry")
def registry_agents():
    if not shared_registry or not _CORE_LOADED:
        return {"agents": []}
    return {"agents": shared_registry.all_agents()}


@app.post("/registry/register")
def registry_register(payload: dict):
    """Agents call this to self-register with skills."""
    name   = (payload or {}).get("name", "")
    skills = (payload or {}).get("skills", [])
    port   = (payload or {}).get("port", 0)
    if not name or not skills:
        return {"ok": False, "error": "name and skills required"}
    if shared_registry and _CORE_LOADED:
        shared_registry.register(name, skills, port)
        _push_update("agent_registered", {"name": name, "skills": skills})
    return {"ok": True}


# ── Snapshot (replaces polling /status) ──────────────────────────────────────

@app.get("/snapshot")
def snapshot():
    """Full state snapshot — used by SwarmPanel fallback polling."""
    return _build_snapshot()


# ── Parallel sessions (gated by PARALLEL_SESSIONS_ENABLED) ────────────────────

def _sm_required():
    if session_manager is None:
        return {"ok": False,
                "error": "parallel sessions disabled — set SWARM_PARALLEL_SESSIONS=1 and restart"}
    return None


@app.post("/route")
def route_prompt(payload: dict):
    """Main entry for parallel-session routing. Body: {prompt, project_path?, target_agent?}"""
    err = _sm_required()
    if err:
        return err
    prompt = (payload or {}).get("prompt", "").strip()
    if not prompt:
        return {"ok": False, "error": "prompt is required"}
    return session_manager.route_prompt(
        prompt=prompt,
        project_path=payload.get("project_path", ""),
        target_agent=payload.get("target_agent", "planner"),
    )


@app.get("/sessions")
def list_sessions():
    err = _sm_required()
    if err:
        return err
    return {"ok": True, "sessions": session_manager.list_sessions()}


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    err = _sm_required()
    if err:
        return err
    s = session_manager.get_session(session_id)
    if not s:
        return {"ok": False, "error": "not found"}
    return {"ok": True, "session": s}


@app.post("/sessions/{session_id}/amend")
def amend_session(session_id: str, payload: dict):
    err = _sm_required()
    if err:
        return err
    text = (payload or {}).get("text", "").strip()
    if not text:
        return {"ok": False, "error": "text is required"}
    return session_manager.amend_session(session_id, text)


@app.delete("/sessions/{session_id}")
def cancel_session(session_id: str):
    err = _sm_required()
    if err:
        return err
    return session_manager.cancel_session(session_id)


# ── UI API bridge (the SPA at swarm/ui/ calls /api/* paths) ─────────────────

@app.get("/api/agents")
def ui_api_agents():
    """Return agents in the format the swarm UI expects (bridges from /status data)."""
    agents_list = []
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM agents ORDER BY id DESC").fetchall()
        for row in rows:
            d = dict(row)
            d["skills"] = json.dumps(_AGENT_SKILLS.get(d["name"], ["worker"]))
            d["tasks_completed"] = 0
            d["created_at"] = d.get("last_heartbeat") or 0
            d["success_rate"] = 0
            agents_list.append(d)
    # Fallback: if DB is empty but agent_processes has entries, synthesize them
    if not agents_list:
        idx = 0
        with _lock:
            for name, proc in agent_processes.items():
                alive = proc.poll() is None
                idx += 1
                agents_list.append({
                    "id": idx,
                    "name": name,
                    "status": "idle" if alive else "offline",
                    "last_heartbeat": agent_last_heartbeat.get(name) or 0,
                    "port": AGENT_PORTS.get(name, 0),
                    "pid": proc.pid if alive else None,
                    "skills": json.dumps(_AGENT_SKILLS.get(name, ["worker"])),
                    "tasks_completed": 0,
                    "created_at": 0,
                    "success_rate": 0,
                })
    return {"agents": agents_list}


@app.get("/api/agents/{agent_id}/memory")
def ui_api_agent_memory(agent_id: int):
    """Return agent memory (stub — returns empty for now)."""
    return {"memory": []}


@app.post("/api/agents/spawn")
def ui_api_agent_spawn(payload: dict):
    """Spawn a new agent via the UI."""
    skills = (payload or {}).get("skills") or payload.get("required_skills", [])
    if not skills:
        return {"ok": False, "error": "skills list required"}
    name = payload.get("name", f"agent_{int(time.time())}")
    port = 0
    # Check if this is a known agent with a script; if not, register virtually
    if name in AGENT_SCRIPTS:
        proc = _spawn_agent(name)
    else:
        # Virtual agent — just register it in the DB without a subprocess
        proc = None
        if shared_registry:
            shared_registry.register(name, skills, port, spawned=True)
        log.info(f"UI spawned virtual agent {name!r} (skills={skills})")
    with _lock:
        agent_processes[name] = proc if proc else None
        agent_last_heartbeat[name] = time.time()
        agent_missed[name] = 0
        agent_retries[name] = 0
    # Insert into DB
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO agents(name,status,port,pid,last_heartbeat) VALUES(?,?,?,?,?)",
                (name, "idle", port, proc.pid, time.time()),
            )
    except Exception as e:
        log.warning(f"DB insert for agent {name} failed: {e}")
    agent_id = proc.pid if proc else int(time.time() * 1000) % 1000000
    _push_update("agent_spawned", {"id": agent_id, "name": name, "skills": skills})
    return {"ok": True, "id": agent_id, "name": name}


@app.post("/api/agents/{name}/status")
@app.patch("/api/agents/{name}/status")
@app.post("/api/agents/{agent_id}/status")
@app.patch("/api/agents/{agent_id}/status")
def ui_api_agent_status(name: str = "", agent_id: str = "", payload: dict = {}):
    """Toggle agent status (pause/resume from UI)."""
    agent_name = name or agent_id
    # If numeric, resolve from DB
    if agent_name.isdigit():
        try:
            with get_connection() as conn:
                row = conn.execute("SELECT name FROM agents WHERE id=?", (int(agent_name),)).fetchone()
                if row:
                    agent_name = row["name"]
        except Exception:
            pass
    new_status = (payload or {}).get("status", "idle")
    log.info(f"UI set agent {agent_name} status -> {new_status}")
    return {"ok": True}


@app.delete("/api/agents/{name}")
@app.delete("/api/agents/{agent_id}")
def ui_api_agent_kill(name: str = "", agent_id: str = ""):
    """Kill an agent from the UI."""
    agent_name = name or agent_id
    # If numeric, resolve from DB
    if agent_name.isdigit():
        try:
            with get_connection() as conn:
                row = conn.execute("SELECT name FROM agents WHERE id=?", (int(agent_name),)).fetchone()
                if row:
                    agent_name = row["name"]
        except Exception:
            pass
    """Kill an agent from the UI."""
    with _lock:
        proc = agent_processes.pop(name, None)
        agent_last_heartbeat.pop(name, None)
        agent_missed.pop(name, None)
        agent_retries.pop(name, None)
    if proc and proc.poll() is None:
        proc.terminate()
        log.info(f"Agent {name} killed by UI")
    try:
        with get_connection() as conn:
            conn.execute("UPDATE agents SET status='retired' WHERE name=?", (name,))
    except Exception:
        pass
    _push_update("agent_stopped", {"id": name})
    return {"ok": True, "message": f"Agent {name} terminated"}


@app.post("/api/tasks")
def ui_api_submit_task(payload: dict):
    """Submit a task from the UI (bridges to /submit logic)."""
    description = (payload or {}).get("description", "").strip()
    if not description:
        return {"ok": False, "error": "description is required"}
    required_skills = (payload or {}).get("required_skills", [])
    target_agent = payload.get("target_agent")
    if not target_agent and required_skills:
        # Map first skill to an agent name
        primary = required_skills[0].lower()
        for agent_name, skills in _AGENT_SKILLS.items():
            if primary in [s.lower() for s in skills]:
                target_agent = agent_name
                break
    if not target_agent:
        target_agent = "planner"
    # Write task to queue
    import uuid as _uuid
    task_id = _uuid.uuid4().hex[:8]
    task_file = TASKS_QUEUE / f"{time.time():.6f}_{task_id}.json"
    TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
    task_file.write_text(
        json.dumps({
            "description": description,
            "target_agent": target_agent,
            "project_path": payload.get("project_path", ""),
            "skills": required_skills,
        }),
        encoding="utf-8",
    )
    log.info(f"UI submitted task [{task_id}] → {target_agent}: {description[:60]}")
    _push_update("task_posted", {"id": task_id, "description": description})
    return {"ok": True, "task_id": task_id, "target_agent": target_agent}


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
        [AGENT_PYTHON, str(script)],
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

    # Attach session linkage if this task came from the SessionManager.
    sid = data.get("session_id")
    if sid and session_manager is not None:
        try:
            session_manager.attach_task(sid, task_id, agent)
        except Exception as e:
            log.warning(f"attach_task failed: {e}")

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
    _startup()
    log.info(f"Orchestrator listening on port {ORCHESTRATOR_PORT}")
    uvicorn.run(app, host="127.0.0.1", port=ORCHESTRATOR_PORT, log_level="warning")
