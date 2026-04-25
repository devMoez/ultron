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
import logging
import sys
import time
import uuid
from pathlib import Path

# Route all logging to stderr only — stdout is the MCP JSON-RPC wire, never log to it
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [mcp] %(levelname)s %(message)s",
    stream=sys.stderr,
    force=True,
)

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
                "Submit a task to the Ultron swarm. The swarm will automatically detect "
                "whether this is a new task (starts a fresh parallel session, up to 5 "
                "concurrent) or an amendment to something already running (merges it). "
                "Use 'planner' when unsure – it breaks the task into subtasks automatically."
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
            name="list_sessions",
            description="List all active parallel sessions (up to 5 can run at once).",
            inputSchema={"type": "object", "properties": {}, "required": []},
        ),
        Tool(
            name="cancel_session",
            description="Cancel a running session by its session ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "Session ID to cancel"},
                },
                "required": ["session_id"],
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
        # Aliases with swarm_ prefix for backward compatibility
        Tool(name="swarm_submit_task", description="Alias for submit_task", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="swarm_get_status", description="Alias for get_status", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="swarm_list_tasks", description="Alias for list_tasks", inputSchema={"type": "object", "properties": {}, "required": []}),
        Tool(name="swarm_launch_swarm_tui", description="Alias for launch_swarm_tui", inputSchema={"type": "object", "properties": {}, "required": []}),
    ]


# ── Tool implementations ──────────────────────────────────────────────────────

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    # Support both "submit_task" and "swarm_submit_task"
    if name.startswith("swarm_"):
        name = name[6:]  # strip "swarm_" prefix
    
    if name == "submit_task":
        return await _submit_task(arguments)
    elif name == "get_status":
        return await _get_status()
    elif name == "list_tasks":
        return await _list_tasks(arguments)
    elif name == "list_sessions":
        return await _list_sessions()
    elif name == "cancel_session":
        return await _cancel_session(arguments)
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

    # ── Try smart multi-session routing via orchestrator /route ──────────────
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(
                f"{ORCHESTRATOR_URL}/route",
                json={
                    "prompt":       description,
                    "target_agent": target_agent,
                    "project_path": project_path,
                },
            )
            if r.status_code == 200:
                data = r.json()
                routing = data.get("routing", {})
                decision = routing.get("decision", "NEW")
                sid = data.get("session_id", "")
                status = data.get("status", "active")
                queue_pos = data.get("queue_pos", "")

                if data.get("needs_clarification"):
                    active = data.get("active", [])
                    sessions_txt = "\n".join(
                        f"  • [{s['id']}] {s['prompt'][:60]} ({s['status']})"
                        for s in active
                    )
                    return [TextContent(type="text", text=(
                        "⚠️ Ambiguous — could be a new task or an edit to a running one.\n\n"
                        f"Active sessions:\n{sessions_txt}\n\n"
                        "To amend a running session, start with 'also', 'change that', or similar.\n"
                        "To force a new session, re-submit with a clearer subject."
                    ))]

                if decision == "EDIT":
                    return [TextContent(type="text", text=(
                        f"✏️ Amendment merged into session `{sid}`\n"
                        f"   Mode: {data.get('mode', 'planner_replan')}\n"
                        f"   Current agent: {data.get('current_agent', '?')}\n"
                        f"   The planner will re-plan and inject your change mid-flight."
                    ))]

                queue_line = f"\n   Queue position: {queue_pos}" if queue_pos else ""
                return [TextContent(type="text", text=(
                    f"✅ {'Queued' if status == 'queued' else 'Started'}: session `{sid}`\n"
                    f"   Agent: {target_agent}\n"
                    f"   Description: {description[:100]}\n"
                    f"   Project: {project_path or '(none)'}{queue_line}\n\n"
                    f"Use `list_sessions` to track up to 5 parallel sessions."
                ))]
    except Exception:
        pass  # orchestrator not up — fall through to queue-file fallback

    # ── Fallback: drop a queue file (orchestrator picks it up when it starts) ─
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

    return [TextContent(type="text", text=(
        f"⚠️ Orchestrator offline — task saved to queue: {filename}\n"
        f"   Agent: {target_agent}\n"
        f"   Description: {description}\n\n"
        f"Start the swarm (start.ps1) and it will be picked up automatically."
    ))]


async def _list_sessions() -> list[TextContent]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{ORCHESTRATOR_URL}/sessions")
            sessions = r.json().get("sessions", [])
    except Exception as e:
        return [TextContent(type="text", text=f"⚠️ Orchestrator offline: {e}")]

    if not sessions:
        return [TextContent(type="text", text="No active sessions.")]

    icons = {"active": "▶️", "queued": "⏸️", "done": "✅", "failed": "❌",
             "paused": "⏸️", "cancelled": "🚫"}
    lines = ["## Parallel Sessions\n"]
    for s in sessions:
        icon = icons.get(s["status"], "❓")
        amends = len(s.get("amendments", []))
        lines.append(
            f"{icon} `{s['id']}` [{s['status']}] → {s['current_agent'] or '?'}\n"
            f"   {s['prompt'][:80]}"
            + (f"\n   {amends} amendment(s)" if amends else "")
        )
    return [TextContent(type="text", text="\n".join(lines))]


async def _cancel_session(args: dict) -> list[TextContent]:
    sid = args.get("session_id", "")
    if not sid:
        return [TextContent(type="text", text="Error: session_id required")]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.delete(f"{ORCHESTRATOR_URL}/sessions/{sid}")
            data = r.json()
    except Exception as e:
        return [TextContent(type="text", text=f"⚠️ Orchestrator offline: {e}")]
    if data.get("ok"):
        return [TextContent(type="text", text=f"✅ Session `{sid}` cancelled.")]
    return [TextContent(type="text", text=f"❌ {data.get('error', 'unknown error')}")]


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
