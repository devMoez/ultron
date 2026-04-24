"""
Ultron Swarm TUI — real-time monitor for the multi-agent swarm.
Polls orchestrator /status every 2 seconds.

Keys:
  q   — quit
  r   — force refresh
  l   — log selector (pick which agent's log to tail)
  1   — focus agents panel
  2   — focus tasks panel
  3   — focus logs panel
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
    DataTable, Footer, Header, Label, Log, Select, Static
)
from textual.timer import Timer

SWARM_ROOT = Path(__file__).resolve().parent
LOGS_DIR   = SWARM_ROOT / "logs"
ORCH_URL   = "http://127.0.0.1:5000"
POLL_SEC   = 2

AGENT_NAMES = ["orchestrator", "planner", "designer", "builder", "debugger", "verifier"]

# ── Status panel ──────────────────────────────────────────────────────────────

class AgentsTable(Static):
    DEFAULT_CSS = """
    AgentsTable {
        border: solid $accent;
        height: 100%;
        padding: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("[bold]Agents[/bold]", id="agents-title")
        yield DataTable(id="agents-table", show_cursor=False)

    def on_mount(self) -> None:
        table = self.query_one("#agents-table", DataTable)
        table.add_columns("Agent", "Status", "Port", "Last HB", "Restarts")

    def update(self, agents: dict) -> None:
        table = self.query_one("#agents-table", DataTable)
        table.clear()
        for name, info in agents.items():
            alive = info.get("alive", False)
            status_icon = "🟢" if alive else "🔴"
            status = f"{status_icon} {'alive' if alive else 'DOWN'}"
            port = str(info.get("port", ""))
            last_hb = info.get("last_hb")
            if last_hb:
                age = int(time.time() - last_hb)
                hb_str = f"{age}s ago"
            else:
                hb_str = "—"
            restarts = str(info.get("retries", 0))
            table.add_row(name, status, port, hb_str, restarts)


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
        icons = {"done": "✅", "failed": "❌", "assigned": "⏳", "queued": "📋"}
        for t in tasks[:10]:
            icon = icons.get(t.get("status", ""), "❓")
            status = f"{icon} {t.get('status','')}"
            desc = (t.get("description") or "")[:50]
            table.add_row(
                str(t.get("id", "")),
                t.get("assigned_agent", ""),
                status,
                desc,
            )


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
        yield Label(f"[bold]Logs — {self.selected_agent}[/bold]", id="log-title")
        yield Log(id="log-view", auto_scroll=True, max_lines=200)

    def tail(self, agent: str, lines: int = 10) -> None:
        self.selected_agent = agent
        self.query_one("#log-title", Label).update(f"[bold]Logs — {agent}[/bold]")
        log_view = self.query_one("#log-view", Log)
        log_file = LOGS_DIR / f"{agent}.log"
        if not log_file.exists():
            log_view.clear()
            log_view.write_line(f"No log file: {log_file}")
            return
        try:
            content = log_file.read_text(encoding="utf-8", errors="replace")
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
    Screen {
        layout: vertical;
    }
    #top-row {
        height: 55%;
        layout: horizontal;
    }
    #bottom-row {
        height: 45%;
    }
    AgentsTable {
        width: 50%;
    }
    TasksTable {
        width: 50%;
    }
    #status-bar {
        height: 1;
        background: $surface;
        color: $text-muted;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("l", "select_log", "Log source"),
        Binding("1", "focus_agents", "Agents"),
        Binding("2", "focus_tasks", "Tasks"),
        Binding("3", "focus_logs", "Logs"),
    ]

    _last_status: str = "Connecting..."
    _timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="top-row"):
            yield AgentsTable(id="agents-panel")
            yield TasksTable(id="tasks-panel")
        yield LogPanel(id="log-panel")
        yield Label(self._last_status, id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        self._timer = self.set_interval(POLL_SEC, self._poll)
        self.call_after_refresh(self._poll)

    async def _poll(self) -> None:
        status_bar = self.query_one("#status-bar", Label)
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                r = await client.get(f"{ORCH_URL}/status")
                data = r.json()

            agents = data.get("agents", {})
            tasks  = data.get("recent_tasks", [])

            self.query_one(AgentsTable).update(agents)
            self.query_one(TasksTable).update(tasks)

            # Refresh log panel
            log_panel = self.query_one(LogPanel)
            log_panel.tail(log_panel.selected_agent)

            alive = sum(1 for a in agents.values() if a.get("alive"))
            total = len(agents)
            now   = datetime.now().strftime("%H:%M:%S")
            status_bar.update(
                f"[green]●[/green] Orchestrator online | {alive}/{total} agents alive | Updated {now}"
            )

        except Exception as e:
            status_bar.update(
                f"[red]●[/red] Orchestrator unreachable ({e}) — is swarm running? (start.ps1)"
            )

    def action_refresh(self) -> None:
        self.call_after_refresh(self._poll)

    def action_focus_agents(self) -> None:
        self.query_one("#agents-panel").focus()

    def action_focus_tasks(self) -> None:
        self.query_one("#tasks-panel").focus()

    def action_focus_logs(self) -> None:
        self.query_one("#log-panel").focus()

    def action_select_log(self) -> None:
        """Cycle through agent logs."""
        panel = self.query_one(LogPanel)
        current = panel.selected_agent
        idx = AGENT_NAMES.index(current) if current in AGENT_NAMES else 0
        next_agent = AGENT_NAMES[(idx + 1) % len(AGENT_NAMES)]
        panel.tail(next_agent)


if __name__ == "__main__":
    SwarmTUI().run()
