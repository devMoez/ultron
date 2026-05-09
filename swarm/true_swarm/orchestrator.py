"""
True Swarm Orchestrator with UI serving.
"""
import asyncio
import json
import time
import threading
from pathlib import Path
from typing import List, Optional
import logging

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .db import get_connection, init_db
from .blackboard import Blackboard
from .skill_library import SkillLibrary
from .agent import TrueSwarmAgent

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger("TrueSwarmOrchestrator")

init_db()

app = FastAPI(title="Ultron True Swarm")

ui_dir = Path(__file__).parent / "ui"
if ui_dir.exists():
    app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")

@app.get("/", response_class=HTMLResponse)
async def root():
    ui_path = ui_dir / "index.html"
    if ui_path.exists():
        return ui_path.read_text(encoding="utf-8")
    return "<h1>Ultron True Swarm</h1>"

# ── WebSocket broadcaster ──────────────────────────────────────────────────────

_ws_clients: list[WebSocket] = []
_ws_lock = threading.Lock()

async def _broadcast(event: dict):
    msg = json.dumps(event)
    dead = []
    with _ws_lock:
        clients = list(_ws_clients)
    for ws in clients:
        try:
            await ws.send_text(msg)
        except Exception:
            dead.append(ws)
    if dead:
        with _ws_lock:
            for ws in dead:
                if ws in _ws_clients:
                    _ws_clients.remove(ws)

def broadcast_sync(event: dict):
    """Thread-safe broadcast from non-async contexts."""
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(_broadcast(event), loop)
    except Exception:
        pass

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    with _ws_lock:
        _ws_clients.append(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive
    except WebSocketDisconnect:
        with _ws_lock:
            if ws in _ws_clients:
                _ws_clients.remove(ws)

# ── In-memory agent registry ───────────────────────────────────────────────────

blackboard = Blackboard()
skill_lib  = SkillLibrary()
agents: dict[int, TrueSwarmAgent] = {}
_agents_lock = threading.Lock()

# ── Request/response models ────────────────────────────────────────────────────

class SpawnRequest(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None

class TaskRequest(BaseModel):
    description: str
    required_skills: Optional[List[str]] = None
    priority: int = 0
    project_path: str = ""

class StatusPatch(BaseModel):
    status: str  # paused | idle

# ── Agent endpoints ────────────────────────────────────────────────────────────

@app.get("/api/agents")
async def list_agents():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name, skills, status, success_rate, tasks_completed, created_at, last_heartbeat FROM agents ORDER BY created_at DESC"
        ).fetchall()
    return {"agents": [dict(r) for r in rows]}


@app.post("/api/agents/spawn")
async def spawn_agent(req: SpawnRequest = SpawnRequest()):
    agent = TrueSwarmAgent(name=req.name)
    if req.skills:
        agent.update_skills(req.skills)
    agent.start()
    with _agents_lock:
        agents[agent.agent_id] = agent
    broadcast_sync({"type": "agent_spawned", "id": agent.agent_id, "name": agent.name, "skills": req.skills or []})
    logger.info(f"Spawned agent {agent.name} (ID {agent.agent_id})")
    return {"id": agent.agent_id, "name": agent.name}


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name, skills, status, success_rate, tasks_completed, created_at, last_heartbeat FROM agents WHERE id = ?",
            (agent_id,)
        ).fetchone()
    if not row:
        raise HTTPException(404, "Agent not found")
    return dict(row)


@app.get("/api/agents/{agent_id}/memory")
async def get_agent_memory(agent_id: int, limit: int = 50):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT timestamp, event_type, data FROM episodic_memory WHERE agent_id = ? ORDER BY timestamp DESC LIMIT ?",
            (agent_id, limit)
        ).fetchall()
    return {"memory": [dict(r) for r in rows]}


@app.patch("/api/agents/{agent_id}/status")
async def patch_agent_status(agent_id: int, req: StatusPatch):
    allowed = {"paused", "idle"}
    if req.status not in allowed:
        raise HTTPException(400, f"status must be one of {allowed}")
    with get_connection() as conn:
        conn.execute("UPDATE agents SET status = ? WHERE id = ?", (req.status, agent_id))
        conn.commit()
    with _agents_lock:
        agent = agents.get(agent_id)
    if agent:
        if req.status == "paused":
            agent.running = False
        else:
            agent.running = True
            agent.start()
    broadcast_sync({"type": "agent_status", "id": agent_id, "status": req.status})
    return {"ok": True, "id": agent_id, "status": req.status}


@app.delete("/api/agents/{agent_id}")
async def stop_agent(agent_id: int):
    with _agents_lock:
        agent = agents.pop(agent_id, None)
    if agent:
        agent.stop()
    with get_connection() as conn:
        conn.execute("UPDATE agents SET status = 'retired' WHERE id = ?", (agent_id,))
        conn.commit()
    broadcast_sync({"type": "agent_stopped", "id": agent_id})
    return {"ok": True}

# ── Task endpoints ─────────────────────────────────────────────────────────────

@app.post("/api/tasks")
async def create_task(req: TaskRequest):
    task_id = blackboard.post_task(
        req.description,
        req.required_skills or [],
        req.priority,
        req.project_path,
    )
    broadcast_sync({"type": "task_posted", "id": task_id, "description": req.description})
    return {"task_id": task_id, "description": req.description}


@app.get("/api/tasks")
async def list_tasks(status: str = "all", limit: int = 50):
    with get_connection() as conn:
        if status == "all":
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit)
            ).fetchall()
    return {"tasks": [dict(r) for r in rows]}


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        raise HTTPException(404, "Task not found")
    return dict(row)

# ── Background manager ─────────────────────────────────────────────────────────

_running = False

def _manager_loop():
    while _running:
        try:
            # Heartbeat check — mark agents offline if stale
            stale_cutoff = time.time() - 30
            with get_connection() as conn:
                conn.execute(
                    "UPDATE agents SET status = 'offline' WHERE status NOT IN ('idle','busy','retired') OR (last_heartbeat < ? AND status = 'busy')",
                    (stale_cutoff,)
                )
                conn.commit()
            time.sleep(10)
        except Exception as e:
            logger.error(f"Manager loop error: {e}")
            time.sleep(10)


def start_background():
    global _running
    if _running:
        return
    _running = True
    threading.Thread(target=_manager_loop, daemon=True).start()


def stop_background():
    global _running
    _running = False


if __name__ == "__main__":
    start_background()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
