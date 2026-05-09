"""
True Swarm MCP Server
Exposes the true swarm to Ultron via MCP stdio protocol.

Tools:
  swarm_status()                           → agent + task overview
  spawn_agent(name?, skills?)              → create a new worker agent
  post_task(description, skills?, priority?, project_path?)  → add task to blackboard
  list_agents()                            → all agents with status
  list_tasks(status?)                      → tasks filtered by status
  stop_agent(id)                           → retire an agent
  get_agent_memory(id, limit?)             → episodic memory for one agent
"""
import asyncio
import json
import sys
import time
from pathlib import Path

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

SWARM_URL = "http://127.0.0.1:8000"

server = Server("ultron-true-swarm")


# ── helpers ───────────────────────────────────────────────────────────────────

async def get(path: str) -> dict:
    async with httpx.AsyncClient(timeout=8.0) as c:
        r = await c.get(f"{SWARM_URL}{path}")
        r.raise_for_status()
        return r.json()

async def post(path: str, body: dict) -> dict:
    async with httpx.AsyncClient(timeout=8.0) as c:
        r = await c.post(f"{SWARM_URL}{path}", json=body)
        r.raise_for_status()
        return r.json()

async def delete(path: str) -> dict:
    async with httpx.AsyncClient(timeout=8.0) as c:
        r = await c.delete(f"{SWARM_URL}{path}")
        r.raise_for_status()
        return r.json()

def fmt(data) -> str:
    return json.dumps(data, indent=2)

def offline_msg() -> list[TextContent]:
    return [TextContent(type="text", text=(
        "⚠️ True Swarm is offline.\n"
        "Start it with: powershell -ExecutionPolicy Bypass -File swarm\\true_swarm\\start.ps1"
    ))]


# ── tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="swarm_status",
            description="Overall true swarm health — agent count, active workers, queued tasks. Call this first.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="spawn_agent",
            description="Spawn a new homogeneous worker agent. Agents bid on tasks that match their skills.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name":   {"type": "string",  "description": "Optional agent name (auto-generated if omitted)"},
                    "skills": {"type": "array", "items": {"type": "string"},
                               "description": "Skills this agent has, e.g. ['code', 'python', 'filesystem']"},
                },
                "required": [],
            },
        ),
        Tool(
            name="post_task",
            description=(
                "Post a task to the blackboard. Any idle agent with matching skills will claim and execute it. "
                "required_skills filters which agents can take it — leave empty to allow any agent."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description":    {"type": "string"},
                    "required_skills": {"type": "array", "items": {"type": "string"},
                                       "description": "Skills an agent must have to claim this task"},
                    "priority":       {"type": "integer", "description": "0–10, higher = claimed first", "default": 0},
                    "project_path":   {"type": "string",  "description": "Absolute path for file-system tasks", "default": ""},
                },
                "required": ["description"],
            },
        ),
        Tool(
            name="list_agents",
            description="List all agents with their current status, skills, and task count.",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="list_tasks",
            description="List tasks from the blackboard.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "queued", "claimed", "done", "failed"],
                        "default": "all",
                    },
                    "limit": {"type": "integer", "default": 20},
                },
                "required": [],
            },
        ),
        Tool(
            name="stop_agent",
            description="Retire an agent. It finishes its current task then stops.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "integer", "description": "Agent ID from list_agents"},
                },
                "required": ["agent_id"],
            },
        ),
        Tool(
            name="get_agent_memory",
            description="Get the episodic memory (action log) for a specific agent.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {"type": "integer"},
                    "limit":    {"type": "integer", "default": 20},
                },
                "required": ["agent_id"],
            },
        ),
    ]


# ── tool handlers ─────────────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, args: dict) -> list[TextContent]:
    try:
        if name == "swarm_status":
            return await _swarm_status()
        elif name == "spawn_agent":
            return await _spawn_agent(args)
        elif name == "post_task":
            return await _post_task(args)
        elif name == "list_agents":
            return await _list_agents()
        elif name == "list_tasks":
            return await _list_tasks(args)
        elif name == "stop_agent":
            return await _stop_agent(args)
        elif name == "get_agent_memory":
            return await _get_agent_memory(args)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except httpx.ConnectError:
        return offline_msg()
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {e}")]


async def _swarm_status() -> list[TextContent]:
    agents_data = await get("/api/agents")
    tasks_data  = await get("/api/tasks?limit=10")
    agents = agents_data.get("agents", [])
    tasks  = tasks_data.get("tasks", [])

    idle    = sum(1 for a in agents if a["status"] == "idle")
    busy    = sum(1 for a in agents if a["status"] == "busy")
    offline = sum(1 for a in agents if a["status"] == "offline")
    queued  = sum(1 for t in tasks  if t["status"] == "queued")
    done    = sum(1 for t in tasks  if t["status"] == "done")

    lines = [
        "## True Swarm Status\n",
        f"**Agents:** {len(agents)} total — {busy} busy, {idle} idle, {offline} offline",
        f"**Tasks (last 10):** {queued} queued, {done} done\n",
        "### Recent Tasks",
    ]
    icons = {"queued": "📋", "claimed": "⏳", "done": "✅", "failed": "❌"}
    for t in tasks[:5]:
        lines.append(f"{icons.get(t['status'], '❓')} [{t['id']}] {t['description'][:70]}")

    return [TextContent(type="text", text="\n".join(lines))]


async def _spawn_agent(args: dict) -> list[TextContent]:
    body = {}
    if args.get("name"):   body["name"]   = args["name"]
    if args.get("skills"): body["skills"] = args["skills"]
    res = await post("/api/agents/spawn", body)
    return [TextContent(type="text", text=f"✅ Agent spawned\n   ID: {res['id']}\n   Name: {res['name']}")]


async def _post_task(args: dict) -> list[TextContent]:
    body = {
        "description":     args["description"],
        "required_skills": args.get("required_skills") or [],
        "priority":        args.get("priority", 0),
        "project_path":    args.get("project_path", ""),
    }
    res = await post("/api/tasks", body)
    return [TextContent(type="text", text=f"✅ Task posted\n   ID: {res['task_id']}\n   Description: {res['description']}")]


async def _list_agents() -> list[TextContent]:
    data   = await get("/api/agents")
    agents = data.get("agents", [])
    if not agents:
        return [TextContent(type="text", text="No agents registered. Use spawn_agent to create one.")]
    icons = {"idle": "🟡", "busy": "🟢", "offline": "🔴", "retired": "⚫", "paused": "⏸️"}
    lines = ["## Agents\n"]
    for a in agents:
        skills = json.loads(a["skills"]) if a.get("skills") else []
        lines.append(
            f"{icons.get(a['status'], '❓')} **{a['name']}** (ID {a['id']}) — {a['status']}\n"
            f"   Skills: {', '.join(skills) or 'none'} | Tasks done: {a['tasks_completed']} | "
            f"Success rate: {(a['success_rate'] or 0)*100:.0f}%"
        )
    return [TextContent(type="text", text="\n".join(lines))]


async def _list_tasks(args: dict) -> list[TextContent]:
    status = args.get("status", "all")
    limit  = args.get("limit", 20)
    data   = await get(f"/api/tasks?status={status}&limit={limit}")
    tasks  = data.get("tasks", [])
    if not tasks:
        return [TextContent(type="text", text=f"No tasks (filter: {status}).")]
    icons = {"queued": "📋", "claimed": "⏳", "done": "✅", "failed": "❌"}
    lines = [f"## Tasks (filter: {status})\n"]
    for t in tasks:
        result_line = f"\n   Result: {str(t.get('result',''))[:80]}" if t.get("result") else ""
        lines.append(
            f"{icons.get(t['status'], '❓')} ID {t['id']} | {t['status']} | "
            f"agent: {t.get('assigned_agent') or '—'}\n"
            f"   {t['description'][:80]}{result_line}"
        )
    return [TextContent(type="text", text="\n".join(lines))]


async def _stop_agent(args: dict) -> list[TextContent]:
    aid = args.get("agent_id")
    if not aid:
        return [TextContent(type="text", text="agent_id required")]
    await delete(f"/api/agents/{aid}")
    return [TextContent(type="text", text=f"✅ Agent {aid} retired.")]


async def _get_agent_memory(args: dict) -> list[TextContent]:
    aid   = args.get("agent_id")
    limit = args.get("limit", 20)
    data  = await get(f"/api/agents/{aid}/memory?limit={limit}")
    mem   = data.get("memory", [])
    if not mem:
        return [TextContent(type="text", text="No memory entries yet.")]
    lines = [f"## Agent {aid} Memory (last {limit})\n"]
    for m in mem:
        d = json.loads(m["data"]) if m.get("data") else {}
        ts = time.strftime("%H:%M:%S", time.localtime(m["timestamp"]))
        lines.append(f"`{ts}` [{m['event_type']}] {json.dumps(d)[:100]}")
    return [TextContent(type="text", text="\n".join(lines))]


# ── entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
