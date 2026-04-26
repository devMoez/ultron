"""
Ultron Swarm TUI — real-time monitor for the multi-agent swarm.
Polls orchestrator /snapshot every 2 seconds.

Keys:
  q        — quit
  r        — force refresh
  l        — cycle log source
  s        — spawn new agent (prompts for skills)
  k        — kill selected agent
  p        — pause/resume selected agent
  a        — assign task to selected agent
  d        — toggle DAG panel
  b        — toggle Bus log panel
  1        — focus agents panel
  2        — focus tasks panel
  3        — focus logs panel
  4        — focus DAG panel
  5        — focus bus log panel
"""

import asyncio
import time
from pathlib import Path
from datetime import datetime

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    DataTable, Footer, Header, Input, Label, Log, Select, Static
)
from textual.timer import Timer
from textual.screen import ModalScreen

SWARM_ROOT = Path(__file__).resolve().parent
LOGS_DIR   = SWARM_ROOT / "logs"
ORCH_URL   = "http://127.0.0.1:5000"
POLL_SEC   = 2

AGENT_NAMES = ["orchestrator", "planner", "designer", "builder", "debugger", "verifier"]


# ── Modal dialogs ─────────────────────────────────────────────────────────────

class SpawnDialog(ModalScreen):
    """Modal to spawn a new agent."""
    DEFAULT_CSS = """
    SpawnDialog {
        align: center middle;
    }
    #spawn-box {
        width: 60;
        height: 12;
        background: $surface;
        border: solid $accent;
        padding: 1 2;
    }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id="spawn-box"):
            yield Label("[bold]Spawn New Agent[/bold]")
            yield Label("Name (leave blank for auto):")
            yield Input(placeholder="e.g. my_coder", id="inp-name")
            yield Label("Skills (comma-separated):")
            yield Input(placeholder="e.g. code,debug", id="inp-skills")
            yield Label("Press Enter to confirm, Esc to cancel")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "inp-skills":
            name   = self.query_one("#inp-name", Input).value.strip() or ""
            skills = [s.strip() for s in event.input.value.split(",") if s.strip()]
            self.dismiss({"name": name, "skills": skills})

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)


class TaskDialog(ModalScreen):
    """Modal to assign a task to an agent."""
    DEFAULT_CSS = """
    TaskDialog {
        align: center middle;
    }
    #task-box {
        width: 70;
        height: 10;
        background: $surface;
        border: solid $accent;
        padding: 1 2;
    }
    """
    def __init__(self, agent_name: str):
        super().__init__()
        self._agent = agent_name

    def compose(self) -> ComposeResult:
        with Vertical(id="task-box"):
            yield Label(f"[bold]Assign Task → {self._agent}[/bold]")
            yield Label("Task description:")
            yield Input(placeholder="e.g. Build login endpoint", id="inp-desc")
            yield Label("Press Enter to send, Esc to cancel")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        desc = event.input.value.strip()
        self.dismiss(desc or None)

    def on_key(self, event) -> None:
        if event.key == "escape":
            self.dismiss(None)


# ── Panels ────────────────────────────────────────────────────────────────────

class AgentsTable(Static):
    DEFAULT_CSS = """
    AgentsTable {
        border: solid $accent;
        height: 100%;
        padding: 0 1;
    }
    """
    _selected: str = ""
    _agents_data: dict = {}

    def compose(self) -> ComposeResult:
        yield Label("[bold]Agents[/bold]  (k=kill  p=pause  a=assign  s=spawn)", id="agents-title")
        yield DataTable(id="agents-table", cursor_type="row")

    def on_mount(self) -> None:
        table = self.query_one("#agents-table", DataTable)
        table.add_columns("Agent", "Skills", "Status", "Port", "Last HB", "Task")

    def update(self, agents: dict) -> None:
        self._agents_data = agents
        table = self.query_one("#agents-table", DataTable)
        table.clear()
        for name, info in agents.items():
            alive  = info.get("alive", False)
            status = info.get("status", "alive" if alive else "offline")
            icon   = {"idle": "🟢", "busy": "🔵", "paused": "🟡", "offline": "🔴"}.get(status, "⚪")
            skills = ", ".join(info.get("skills", []))[:20] or "—"
            port   = str(info.get("port", ""))
            last_hb = info.get("last_hb")
            hb_str  = f"{int(time.time()-last_hb)}s ago" if last_hb else "—"
            task    = (info.get("current_task") or "")[:30]
            table.add_row(name, skills, f"{icon} {status}", port, hb_str, task)

    def selected_agent(self) -> str:
        table = self.query_one("#agents-table", DataTable)
        if table.cursor_row < 0:
            return ""
        keys = list(self._agents_data.keys())
        idx  = table.cursor_row
        return keys[idx] if idx < len(keys) else ""


class TasksTable(Static):
    DEFAULT_CSS = """
    TasksTable {
        border: solid $accent;
        height: 100%;
        padding: 0 1;
    }
    """
    def compose(self) -> ComposeResult:
        yield Label("[bold]Recent Tasks[/bold]", id="tasks-title")
        yield DataTable(id="tasks-table", show_cursor=False)

    def on_mount(self) -> None:
        table = self.query_one("#tasks-table", DataTable)
        table.add_columns("ID", "Agent", "Status", "Description")

    def update(self, tasks: list) -> None:
        table = self.query_one("#tasks-table", DataTable)
        table.clear()
        icons = {"done": "✅", "failed": "❌", "assigned": "⏳", "queued": "📋",
                 "running": "🔵", "pending": "⬜", "ready": "🟡"}
        for t in tasks[:15]:
            icon   = icons.get(t.get("status", ""), "❓")
            status = f"{icon} {t.get('status','')}"
            desc   = (t.get("description") or "")[:50]
            table.add_row(str(t.get("id", "")), t.get("assigned_agent", ""), status, desc)


class DAGPanel(Static):
    DEFAULT_CSS = """
    DAGPanel {
        border: solid $warning;
        height: 100%;
        padding: 0 1;
    }
    """
    def compose(self) -> ComposeResult:
        yield Label("[bold]Task DAG[/bold]", id="dag-title")
        yield Log(id="dag-view", auto_scroll=False, max_lines=100)

    def update(self, nodes: list, edges: list) -> None:
        view = self.query_one("#dag-view", Log)
        view.clear()
        # Build adjacency for display
        deps: dict[str, list[str]] = {}
        for e in edges:
            deps.setdefault(e["to"], []).append(e["from"])
        status_icons = {"done": "✓", "failed": "✗", "running": "→",
                        "assigned": "⟳", "ready": "▶", "pending": "·"}
        for node in nodes:
            icon  = status_icons.get(node.get("status", ""), "?")
            tid   = node.get("id", "")[:8]
            desc  = (node.get("description") or "")[:45]
            agent = node.get("assigned_agent") or ""
            dep_ids = deps.get(tid, [])
            dep_str = f" ← [{','.join(dep_ids)}]" if dep_ids else ""
            view.write_line(f"{icon} {tid} [{node.get('status',''):8}] {desc}  {agent}{dep_str}")


class BusPanel(Static):
    DEFAULT_CSS = """
    BusPanel {
        border: solid $success;
        height: 100%;
        padding: 0 1;
    }
    """
    def compose(self) -> ComposeResult:
        yield Label("[bold]Agent Bus Log[/bold]", id="bus-title")
        yield Log(id="bus-view", auto_scroll=True, max_lines=200)

    def update(self, entries: list) -> None:
        view = self.query_one("#bus-view", Log)
        view.clear()
        for e in entries[-30:]:
            ts  = datetime.fromtimestamp(e.get("ts", 0)).strftime("%H:%M:%S")
            ch  = e.get("channel", "")
            evt = e.get("event", "")
            agent = e.get("agent", e.get("task_id", ""))
            view.write_line(f"{ts} [{ch}] {evt}  {agent}")


class LogPanel(Static):
    DEFAULT_CSS = """
    LogPanel {
        border: solid $accent;
        height: 100%;
        padding: 0 1;
    }
    """
    selected_agent: reactive[str] = reactive("orchestrator")

    def compose(self) -> ComposeResult:
        yield Label(f"[bold]Logs — {self.selected_agent}[/bold]  (l=cycle)", id="log-title")
        yield Log(id="log-view", auto_scroll=True, max_lines=200)

    def tail(self, agent: str, lines: int = 20) -> None:
        self.selected_agent = agent
        self.query_one("#log-title", Label).update(
            f"[bold]Logs — {agent}[/bold]  (l=cycle)"
        )
        log_view = self.query_one("#log-view", Log)
        log_file = LOGS_DIR / f"{agent}.log"
        if not log_file.exists():
            log_view.clear()
            log_view.write_line(f"No log file: {log_file}")
            return
        try:
            content    = log_file.read_text(encoding="utf-8", errors="replace")
            tail_lines = content.splitlines()[-lines:]
            log_view.clear()
            for line in tail_lines:
                log_view.write_line(line)
        except Exception as e:
            log_view.clear()
            log_view.write_line(f"Error reading log: {e}")


# ── Main app ──────────────────────────────────────────────────────────────────

class SwarmTUI(App):
    TITLE = "Ultron Swarm Monitor"
    CSS = """
    Screen { layout: vertical; }
    #main-row  { height: 50%; layout: horizontal; }
    #mid-row   { height: 25%; layout: horizontal; }
    #bottom-row { height: 25%; }
    AgentsTable { width: 50%; }
    TasksTable  { width: 50%; }
    DAGPanel    { width: 50%; }
    BusPanel    { width: 50%; }
    #status-bar {
        height: 1;
        background: $surface;
        color: $text-muted;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q",     "quit",          "Quit"),
        Binding("r",     "refresh",       "Refresh"),
        Binding("l",     "select_log",    "Cycle logs"),
        Binding("s",     "spawn",         "Spawn agent"),
        Binding("k",     "kill",          "Kill agent"),
        Binding("p",     "pause_resume",  "Pause/Resume"),
        Binding("a",     "assign",        "Assign task"),
        Binding("1",     "focus_agents",  "Agents"),
        Binding("2",     "focus_tasks",   "Tasks"),
        Binding("3",     "focus_logs",    "Logs"),
        Binding("4",     "focus_dag",     "DAG"),
        Binding("5",     "focus_bus",     "Bus"),
    ]

    _last_snapshot: dict = {}
    _timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-row"):
            yield AgentsTable(id="agents-panel")
            yield TasksTable(id="tasks-panel")
        with Horizontal(id="mid-row"):
            yield DAGPanel(id="dag-panel")
            yield BusPanel(id="bus-panel")
        yield LogPanel(id="log-panel")
        yield Label("Connecting...", id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._timer = self.set_interval(POLL_SEC, self._poll)
        self.call_after_refresh(self._poll)

    # ── Polling ───────────────────────────────────────────────────────────────

    async def _poll(self) -> None:
        status_bar = self.query_one("#status-bar", Label)
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(f"{ORCH_URL}/snapshot")
                data = r.json()
            self._last_snapshot = data

            agents   = data.get("agents", {})
            tasks    = data.get("tasks", [])
            dag      = data.get("dag", {})
            bus_log  = data.get("bus_log", [])

            self.query_one(AgentsTable).update(agents)
            self.query_one(TasksTable).update(tasks)
            self.query_one(DAGPanel).update(dag.get("nodes", []), dag.get("edges", []))
            self.query_one(BusPanel).update(bus_log)
            self.query_one(LogPanel).tail(
                self.query_one(LogPanel).selected_agent
            )

            alive = sum(1 for a in agents.values() if a.get("alive") or a.get("status") == "idle")
            total = len(agents)
            now   = datetime.now().strftime("%H:%M:%S")
            status_bar.update(
                f"[green]●[/green] Online | {alive}/{total} agents | "
                f"{len(tasks)} tasks | Updated {now}"
            )
        except Exception as e:
            status_bar.update(
                f"[red]●[/red] Unreachable ({e}) — run: cd swarm && .\\start.ps1"
            )

    # ── Actions ───────────────────────────────────────────────────────────────

    def action_refresh(self) -> None:
        self.call_after_refresh(self._poll)

    def action_focus_agents(self) -> None:
        self.query_one("#agents-panel").focus()

    def action_focus_tasks(self) -> None:
        self.query_one("#tasks-panel").focus()

    def action_focus_logs(self) -> None:
        self.query_one("#log-panel").focus()

    def action_focus_dag(self) -> None:
        self.query_one("#dag-panel").focus()

    def action_focus_bus(self) -> None:
        self.query_one("#bus-panel").focus()

    def action_select_log(self) -> None:
        panel   = self.query_one(LogPanel)
        current = panel.selected_agent
        idx     = AGENT_NAMES.index(current) if current in AGENT_NAMES else 0
        panel.tail(AGENT_NAMES[(idx + 1) % len(AGENT_NAMES)])

    def action_spawn(self) -> None:
        def on_result(result):
            if result and result.get("skills"):
                self.call_after_refresh(lambda: self._do_spawn(result))
        self.push_screen(SpawnDialog(), on_result)

    def action_kill(self) -> None:
        name = self.query_one(AgentsTable).selected_agent()
        if name:
            self.call_after_refresh(lambda: self._do_kill(name))

    def action_pause_resume(self) -> None:
        name = self.query_one(AgentsTable).selected_agent()
        if name:
            agents = self._last_snapshot.get("agents", {})
            status = (agents.get(name) or {}).get("status", "idle")
            if status == "paused":
                self.call_after_refresh(lambda: self._do_resume(name))
            else:
                self.call_after_refresh(lambda: self._do_pause(name))

    def action_assign(self) -> None:
        name = self.query_one(AgentsTable).selected_agent()
        if not name:
            return
        def on_result(desc):
            if desc:
                self.call_after_refresh(lambda: self._do_assign(name, desc))
        self.push_screen(TaskDialog(name), on_result)

    # ── HTTP helpers ──────────────────────────────────────────────────────────

    async def _do_spawn(self, payload: dict) -> None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                await c.post(f"{ORCH_URL}/agents/spawn", json=payload)
        except Exception as e:
            self.query_one("#status-bar", Label).update(f"[red]Spawn failed: {e}[/red]")

    async def _do_kill(self, name: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                await c.post(f"{ORCH_URL}/agents/{name}/kill")
        except Exception as e:
            self.query_one("#status-bar", Label).update(f"[red]Kill failed: {e}[/red]")

    async def _do_pause(self, name: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                await c.post(f"{ORCH_URL}/agents/{name}/pause")
        except Exception as e:
            self.query_one("#status-bar", Label).update(f"[red]Pause failed: {e}[/red]")

    async def _do_resume(self, name: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                await c.post(f"{ORCH_URL}/agents/{name}/resume")
        except Exception as e:
            self.query_one("#status-bar", Label).update(f"[red]Resume failed: {e}[/red]")

    async def _do_assign(self, name: str, desc: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=5.0) as c:
                r = await c.post(f"{ORCH_URL}/agents/{name}/assign",
                                 json={"description": desc})
            data = r.json()
            if data.get("ok"):
                self.query_one("#status-bar", Label).update(
                    f"[green]Task assigned to {name}[/green]"
                )
        except Exception as e:
            self.query_one("#status-bar", Label).update(f"[red]Assign failed: {e}[/red]")


if __name__ == "__main__":
    SwarmTUI().run()
