"""
Ultron Swarm – MCP Server
Exposes swarm tools to Ultron/OpenCode via the MCP stdio protocol.

Tools:
  submit_task(description, target_agent?, project_path?) → task queued
  get_status()                                           → all agent + task states
  list_tasks(limit?)                                     → recent tasks from DB
  get_logs(agent?, lines?)                               → tail agent log file

Started automatically by OpenCode when configured in opencode.json.
Do NOT pre-start this manually – OpenCode manages the process.
"""

import asyncio
import json
import sys
import time
import uuid
from pathlib import Path

# Ensure swarm root is importable
SWARM_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(SWARM_ROOT))

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from swarm_config import (
    AGENT_PORTS, ORCHESTRATOR_PORT, TASKS_QUEUE, LOGS_DIR, DB_PATH
)

ORCHESTRATOR_URL = f"http://127.0.0.1:{ORCHESTRATOR_PORT}"

server = Server("ultron-swarm")


# ── Tool definitions ──────────────────────────────────────────────────────────

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="submit_task",
            description=(
                "Submit a task to the Ultron swarm. The swarm will route it to the "
                "appropriate agent (planner, designer, builder, debugger, or verifier). "
                "Use 'planner' when unsure – it will break the task into subtasks automatically."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "What the swarm should do, e.g. 'build a login page with JWT auth'",
                    },
                    "target_agent": {
                        "type": "string",
                        "enum": ["planner", "designer", "builder", "debugger", "verifier"],
                        "description": "Which agent handles this. Default: planner",
                        "default": "planner",
                    },
                    "project_path": {
                        "type": "string",
                        "description": "Absolute path to the project directory (optional)",
                        "default": "",
                    },
                },
                "required": ["description"],
            },
        ),
        Tool(
            name="get_status",
            description=(
                "Get the current status of all swarm agents and recent tasks. "
                "Use this to check if the swarm is running, what agents are active, "
                "and what tasks are in progress or completed."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_tasks",
            description="List recent tasks from the swarm task database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Max tasks to return (default 10)",
                        "default": 10,
                    },
                    "status": {
                        "type": "string",
                        "enum": ["queued", "assigned", "done", "failed", "all"],
                        "description": "Filter by status (default: all)",
                        "default": "all",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="launch_swarm_tui",
            description=(
                "Launch the Ultron Swarm TUI dashboard in a new terminal window. "
                "Shows real-time agent status, task queue, and logs. Non-blocking."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_logs",
            description="Tail the log file of a swarm agent or the orchestrator.",
            inputSchema={
                "type": "object",
                "properties": {
                    "agent": {
                        "type": "string",
                        "enum": ["orchestrator", "planner", "designer", "builder", "debugger", "verifier"],
                        "description": "Which log to read (default: orchestrator)",
                        "default": "orchestrator",
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Number of lines from end of log (default 50)",
                        "default": 50,
                    },
                },
                "required": [],
            },
        ),
    ]


# ── Tool implementations ──────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "submit_task":
        return await _submit_task(arguments)
    elif name == "get_status":
        return await _get_status()
    elif name == "list_tasks":
        return await _list_tasks(arguments)
    elif name == "launch_swarm_tui":
        return await _launch_swarm_tui()
    elif name == "get_logs":
        return await _get_logs(arguments)
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def _submit_task(args: dict) -> list[TextContent]:
    description  = args.get("description", "")
    target_agent = args.get("target_agent", "planner")
    project_path = args.get("project_path", "")

    if not description:
        return [TextContent(type="text", text="Error: description is required")]

    # Write task JSON to queue folder
    task = {
        "target_agent": target_agent,
        "description":  description,
        "project_path": project_path,
        "submitted_at": time.time(),
        "source":       "ultron-mcp",
    }
    filename = f"task_{uuid.uuid4().hex[:8]}.json"
    task_file = TASKS_QUEUE / filename
    TASKS_QUEUE.mkdir(parents=True, exist_ok=True)
    task_file.write_text(json.dumps(task, indent=2), encoding="utf-8")

    # Also try to ping orchestrator directly (it may not be running yet)
    orch_status = "unknown"
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{ORCHESTRATOR_URL}/status")
            orch_status = "running" if r.status_code == 200 else "error"
    except Exception:
        orch_status = "not running – start the swarm with start.ps1 first"

    return [TextContent(type="text", text=(
        f"✅ Task queued: {filename}\n"
        f"   Agent: {target_agent}\n"
        f"   Description: {description}\n"
        f"   Project: {project_path or '(none)'}\n"
        f"   Orchestrator: {orch_status}\n\n"
        f"The orchestrator will pick this up within 2 seconds and route it to the {target_agent} agent."
    ))]


async def _get_status() -> list[TextContent]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{ORCHESTRATOR_URL}/status")
            data = r.json()
    except Exception as e:
        # Orchestrator not running — show what we can from DB
        return [TextContent(type="text", text=(
            f"⚠️ Orchestrator is not reachable: {e}\n"
            f"Run: powershell -ExecutionPolicy Bypass -File swarm\\start.ps1\n\n"
            f"Expected ports:\n" +
            "\n".join(f"  {name}: 127.0.0.1:{port}" for name, port in AGENT_PORTS.items())
        ))]

    agents = data.get("agents", {})
    tasks  = data.get("recent_tasks", [])

    lines = ["## Swarm Status\n"]
    lines.append("### Agents")
    for name, info in agents.items():
        icon = "🟢" if info.get("alive") else "🔴"
        status = "alive" if info.get("alive") else "DOWN"
        missed = info.get("missed", 0)
        retries = info.get("retries", 0)
        lines.append(f"{icon} **{name}** (port {info.get('port')}) – {status}"
                     + (f" | missed hb: {missed}" if missed else "")
                     + (f" | restarts: {retries}" if retries else ""))

    lines.append("\n### Recent Tasks (last 10)")
    for t in tasks[:10]:
        status_icon = {"done": "✅", "failed": "❌", "assigned": "⏳", "queued": "📋"}.get(t.get("status",""), "❓")
        lines.append(f"{status_icon} [{t.get('id')}] {t.get('assigned_agent')} – {t.get('description','')[:60]}")

    return [TextContent(type="text", text="\n".join(lines))]


async def _list_tasks(args: dict) -> list[TextContent]:
    limit  = int(args.get("limit", 10))
    status = args.get("status", "all")

    if not DB_PATH.exists():
        return [TextContent(type="text", text="Database not initialized yet. Run start.ps1 first.")]

    import sqlite3
    try:
        conn = sqlite3.connect(str(DB_PATH), timeout=5.0)
        conn.row_factory = sqlite3.Row
        if status == "all":
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC LIMIT ?",
                (status, limit)
            ).fetchall()
        conn.close()
    except Exception as e:
        return [TextContent(type="text", text=f"DB error: {e}")]

    if not rows:
        return [TextContent(type="text", text="No tasks found.")]

    lines = [f"## Tasks (filter: {status}, limit: {limit})\n"]
    for r in rows:
        row = dict(r)
        icon = {"done": "✅", "failed": "❌", "assigned": "⏳", "queued": "📋"}.get(row.get("status",""), "❓")
        lines.append(
            f"{icon} ID={row['id']} | {row['assigned_agent']} | {row['status']}\n"
            f"   {row['description'][:80]}\n"
            + (f"   result: {str(row.get('result',''))[:100]}\n" if row.get('result') else "")
        )
    return [TextContent(type="text", text="\n".join(lines))]


async def _launch_swarm_tui() -> list[TextContent]:
    import subprocess
    tui_ps1 = SWARM_ROOT / "swarm-tui.ps1"
    try:
        subprocess.Popen(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(tui_ps1)],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        return [TextContent(type="text", text="TUI launched — swarm dashboard opening in new window.")]
    except Exception as e:
        return [TextContent(type="text", text=f"Failed to launch TUI: {e}")]


async def _get_logs(args: dict) -> list[TextContent]:
    agent = args.get("agent", "orchestrator")
    lines = int(args.get("lines", 50))

    log_file = LOGS_DIR / f"{agent}.log"
    if not log_file.exists():
        return [TextContent(type="text", text=f"Log file not found: {log_file}\nHas the swarm been started?")]

    try:
        content = log_file.read_text(encoding="utf-8", errors="replace")
        tail = "\n".join(content.splitlines()[-lines:])
        return [TextContent(type="text", text=f"## {agent}.log (last {lines} lines)\n\n{tail}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error reading log: {e}")]


# ── Entrypoint ────────────────────────────────────────────────────────────────

async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
