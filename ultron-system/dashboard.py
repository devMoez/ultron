"""Phase 9 — Ultron Master Dashboard (FastAPI, port 5010)."""
import asyncio
import json
import time
from pathlib import Path

import httpx
import psutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from core.config import SWARM_URL, DASHBOARD_PORT, LOGS_DIR, ROOT
from core.logger import get_logger
from core.state import get as state_get, load as state_load
from core import tasks as task_mgr, monitor, memory, intelligence, optimizer, recovery

log = get_logger("dashboard")

state_load()

UI_DIR     = ROOT / "ui"
STATIC_DIR = ROOT / "static"
HTML_FILE  = UI_DIR / "dashboard.html"

# Agent name → port (from swarm_config — duplicated here to avoid import issues)
AGENT_PORTS = {
    "orchestrator": 5000,
    "planner":      5005,
    "designer":     5001,
    "builder":      5002,
    "debugger":     5003,
    "verifier":     5004,
}

app = FastAPI(title="Ultron Master Dashboard")

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── Per-agent process stats ───────────────────────────────────────────────────

# Cache PID → psutil.Process so cpu_percent is accurate (needs 2 calls)
_proc_cache: dict[int, psutil.Process] = {}


def _proc_by_port(port: int):
    """Find the psutil.Process listening on the given port."""
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            # psutil 5.x: proc.connections(), 6.x: proc.net_connections()
            try:
                conns = proc.net_connections(kind="inet")
            except AttributeError:
                conns = proc.connections(kind="inet")
            for c in conns:
                if c.laddr.port == port and c.status in ("LISTEN", "ESTABLISHED", ""):
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def _agent_proc_stats(name: str, port: int) -> dict:
    proc = _proc_by_port(port)
    if proc is None:
        return {"pid": None, "cpu": 0, "ram_mb": 0, "threads": 0,
                "status": "offline", "uptime_s": 0}
    try:
        pid = proc.pid
        # Reuse cached Process object for accurate cpu_percent
        if pid not in _proc_cache:
            _proc_cache[pid] = psutil.Process(pid)
            _proc_cache[pid].cpu_percent()  # first call seeds the counter

        p = _proc_cache[pid]
        mem_info = p.memory_info()
        return {
            "pid":      pid,
            "cpu":      round(p.cpu_percent(), 1),
            "ram_mb":   round(mem_info.rss / 1e6, 1),
            "threads":  p.num_threads(),
            "status":   p.status(),
            "uptime_s": round(time.time() - p.create_time()),
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        _proc_cache.pop(proc.pid, None)
        return {"pid": None, "cpu": 0, "ram_mb": 0, "threads": 0,
                "status": "offline", "uptime_s": 0}


# ── Build payload ─────────────────────────────────────────────────────────────

async def build_payload() -> dict:
    # Swarm agent state from orchestrator
    swarm_agents: dict = {}
    swarm_tasks:  list = []
    swarm_online = False
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{SWARM_URL}/status")
            if r.status_code == 200:
                data = r.json()
                swarm_online  = True
                swarm_agents  = data.get("agents", {})
                swarm_tasks   = data.get("recent_tasks", [])[:30]
    except Exception:
        pass

    # Per-agent combined view: process stats + swarm state
    agents_out = {}
    for name, port in AGENT_PORTS.items():
        proc = _agent_proc_stats(name, port)
        swarm_info = swarm_agents.get(name, {})

        # Current task: look for an assigned task for this agent
        current = next(
            (t for t in swarm_tasks
             if t.get("assigned_agent") == name and t.get("status") == "assigned"),
            None,
        )

        agents_out[name] = {
            "port":         port,
            # Process metrics
            "cpu":          proc["cpu"],
            "ram_mb":       proc["ram_mb"],
            "threads":      proc["threads"],
            "proc_status":  proc["status"],
            "uptime_s":     proc["uptime_s"],
            "pid":          proc["pid"],
            # Swarm state
            "alive":        swarm_info.get("alive", proc["status"] not in ("offline",)),
            "missed_hb":    swarm_info.get("missed", 0),
            "restarts":     swarm_info.get("retries", 0),
            # Task context
            "current_task": current.get("description", "") if current else "",
            "task_id":      current.get("id", "") if current else "",
        }

    # Per-agent task counts from swarm task list
    for name in agents_out:
        agent_tasks = [t for t in swarm_tasks if t.get("assigned_agent") == name]
        agents_out[name]["tasks_done"]     = sum(1 for t in agent_tasks if t["status"] == "done")
        agents_out[name]["tasks_failed"]   = sum(1 for t in agent_tasks if t["status"] == "failed")
        agents_out[name]["tasks_queued"]   = sum(1 for t in agent_tasks if t["status"] == "queued")
        agents_out[name]["tasks_assigned"] = sum(1 for t in agent_tasks if t["status"] == "assigned")

    # Recent logs
    logs = []
    for lname in ("orchestrator", "planner", "builder", "designer", "debugger", "verifier"):
        # Use swarm logs dir
        swarm_log = ROOT.parent / "swarm" / "logs" / f"{lname}.log"
        local_log = LOGS_DIR / f"{lname}.log"
        lf = swarm_log if swarm_log.exists() else local_log
        if lf.exists():
            try:
                lines = lf.read_text(encoding="utf-8", errors="replace").splitlines()[-10:]
                for line in lines:
                    logs.append({"source": lname, "line": line})
            except Exception:
                pass

    # Task stats (local DB)
    try:
        task_stats = task_mgr.stats()
    except Exception:
        task_stats = {}

    # Uptime
    uptime = round(time.time() - (state_get("started_at") or time.time()))

    return {
        "ts":          time.time(),
        "uptime":      uptime,
        "swarm_online": swarm_online,
        "agents":      agents_out,
        "tasks":       swarm_tasks[:20],
        "task_stats":  task_stats,
        "logs":        sorted(logs, key=lambda x: x["line"][:23])[-50:],
    }


# ── SSE stream ────────────────────────────────────────────────────────────────

async def event_stream():
    while True:
        try:
            payload = await build_payload()
            yield f"data: {json.dumps(payload)}\n\n"
        except Exception as e:
            log.error(f"SSE error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        await asyncio.sleep(2)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTML_FILE.read_text(encoding="utf-8")


@app.get("/stream")
async def stream():
    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/snapshot")
async def snapshot():
    return await build_payload()


@app.get("/api/tasks")
async def api_tasks(status: str = "all", limit: int = 50):
    return {"tasks": task_mgr.list_tasks(status=status, limit=limit)}


@app.post("/api/tasks")
async def api_create_task(body: dict):
    tid = task_mgr.create_task(
        title=body.get("title", "Untitled"),
        description=body.get("description", ""),
        priority=body.get("priority", 1),
        agent=body.get("agent", ""),
        tags=body.get("tags", []),
    )
    return {"id": tid}


@app.get("/api/tasks/stats")
async def api_task_stats():
    return task_mgr.stats()


@app.get("/api/monitor/history")
async def api_monitor_history(minutes: int = 60):
    return {"samples": monitor.history(minutes)}


@app.get("/api/intelligence/summary")
async def api_summary(date: str = ""):
    if not date:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
    s = intelligence.load_summary(date)
    if not s:
        s = intelligence.generate_daily_summary()
    return s


@app.get("/api/optimizer/patterns")
async def api_patterns():
    return optimizer.analyze_patterns()


@app.get("/api/recovery/crashes")
async def api_crashes(n: int = 20):
    return {"crashes": recovery.recent_crashes(n)}


@app.get("/api/memory/{layer}")
async def api_memory(layer: str):
    try:
        return {"layer": layer, "data": memory.dump_layer(layer)}
    except ValueError as e:
        return {"error": str(e)}


@app.get("/api/logs/{agent}")
async def api_logs(agent: str, lines: int = 100):
    allowed = {"orchestrator", "dashboard", "planner", "builder",
               "designer", "debugger", "verifier"}
    if agent not in allowed:
        return {"error": "invalid agent"}
    swarm_log = ROOT.parent / "swarm" / "logs" / f"{agent}.log"
    local_log = LOGS_DIR / f"{agent}.log"
    lf = swarm_log if swarm_log.exists() else local_log
    if not lf.exists():
        return {"lines": []}
    return {"lines": lf.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]}


# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    log.info(f"Dashboard starting on http://127.0.0.1:{DASHBOARD_PORT}")
    uvicorn.run(app, host="127.0.0.1", port=DASHBOARD_PORT, log_level="warning")
