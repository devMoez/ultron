"""
Step 8: Debugger Agent – runs tests every 30 seconds and on-demand.
Port: 5003
"""
import subprocess
import sys
import threading
import time
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent
from swarm_config import PROJECTS_DIR, ORCHESTRATOR_URL

POLL_INTERVAL = 30  # seconds


class DebuggerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="debugger", port=5003)
        self._debug_timer: threading.Timer | None = None

    def handle_task(self, task: dict) -> str:
        project_path = task.get("project_path", "")
        return self._run_tests(project_path)

    def _schedule_next(self) -> None:
        self._debug_timer = threading.Timer(POLL_INTERVAL, self._periodic_debug)
        self._debug_timer.daemon = True
        self._debug_timer.start()

    def _periodic_debug(self) -> None:
        """Run tests across all known projects."""
        for project_dir in PROJECTS_DIR.iterdir():
            if project_dir.is_dir():
                result = self._run_tests(str(project_dir))
                self.log(f"[periodic] {project_dir.name}: {result}")
        self._schedule_next()

    def _run_tests(self, project_path: str) -> str:
        if not project_path:
            return "No project path provided"

        p = Path(project_path)
        if not p.exists():
            return f"Project path does not exist: {project_path}"

        tests_dir = p / "tests"
        if not tests_dir.exists() or not any(tests_dir.glob("test_*.py")):
            self.log(f"No tests found in {tests_dir}")
            return "No tests found"

        self.log(f"Running tests in {tests_dir}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short", "-q"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(p),
            )
            output = result.stdout + result.stderr
            if result.returncode == 0:
                self.log(f"Tests PASSED in {project_path}")
                return f"PASSED\n{output[:500]}"
            else:
                self.log(f"Tests FAILED in {project_path}", "warning")
                self._report_failure(project_path, output)
                return f"FAILED\n{output[:500]}"
        except subprocess.TimeoutExpired:
            return "Test run timed out"
        except Exception as e:
            return f"Test error: {e}"

    def _report_failure(self, project_path: str, output: str) -> None:
        import httpx
        try:
            httpx.post(
                f"{ORCHESTRATOR_URL}/task_result",
                json={
                    "agent": self.name,
                    "success": False,
                    "result": f"Tests failed in {project_path}:\n{output[:300]}",
                    "task_id": None,
                },
                timeout=5.0,
            )
        except Exception:
            pass

    def start(self) -> None:
        self.log(f"Starting debugger agent on port {self.port}")
        self._heartbeat_thread.start()
        self._schedule_next()
        import uvicorn
        uvicorn.run(self.app, host="127.0.0.1", port=self.port, log_level="warning")


if __name__ == "__main__":
    DebuggerAgent().start()
