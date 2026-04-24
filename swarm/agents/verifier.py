"""
Step 9: Verifier Agent – runs regression tests after any file change.
Rejects changes if previously passing tests now fail.
Port: 5004
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent
from swarm_config import AGENT_PORTS

# Stores last known test results: {project_path: {test_id: "passed"|"failed"}}
_test_history: dict[str, dict[str, str]] = {}


class VerifierAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="verifier", port=5004)

    def handle_task(self, task: dict) -> str:
        project_path = task.get("project_path", "")
        requesting_agent = task.get("requesting_agent", "")
        return self._verify(project_path, requesting_agent)

    def _verify(self, project_path: str, requesting_agent: str) -> str:
        if not project_path:
            return "No project path"

        p = Path(project_path)
        tests_dir = p / "tests"
        if not tests_dir.exists() or not any(tests_dir.glob("test_*.py")):
            self.log(f"No tests to verify in {tests_dir}")
            return "No tests found – approved by default"

        self.log(f"Verifying {project_path}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short", "--json-report",
                 "--json-report-file=/dev/null"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(p),
            )
        except FileNotFoundError:
            # pytest-json-report not installed, fall back to plain pytest
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(p),
            )

        output = result.stdout + result.stderr
        current_results = self._parse_results(output)
        prev_results = _test_history.get(project_path, {})

        # Regression check: any test that previously PASSED now FAILS?
        regressions = [
            tid for tid, status in current_results.items()
            if status == "FAILED" and prev_results.get(tid) == "PASSED"
        ]

        if regressions:
            self.log(f"REGRESSION detected: {regressions}", "error")
            if requesting_agent:
                self._send_reject(requesting_agent, project_path, regressions)
            return f"REJECTED – regressions: {regressions}"

        # Update history with current results
        _test_history[project_path] = {**prev_results, **current_results}
        self.log(f"Verification APPROVED for {project_path}")
        return "APPROVED"

    def _parse_results(self, output: str) -> dict[str, str]:
        """Parse pytest -v output into {test_id: 'PASSED'|'FAILED'}."""
        results: dict[str, str] = {}
        for line in output.splitlines():
            if " PASSED" in line:
                tid = line.split(" PASSED")[0].strip()
                results[tid] = "PASSED"
            elif " FAILED" in line:
                tid = line.split(" FAILED")[0].strip()
                results[tid] = "FAILED"
        return results

    def _send_reject(self, agent_name: str, project_path: str, regressions: list[str]) -> None:
        import httpx
        port = AGENT_PORTS.get(agent_name)
        if not port:
            return
        try:
            httpx.post(
                f"http://127.0.0.1:{port}/report_status",
                json={
                    "from": "verifier",
                    "verdict": "reject",
                    "project_path": project_path,
                    "regressions": regressions,
                    "message": f"Your change broke {len(regressions)} test(s). Revert with git restore.",
                },
                timeout=5.0,
            )
        except Exception as e:
            self.log(f"Could not send reject to {agent_name}: {e}", "warning")


if __name__ == "__main__":
    VerifierAgent().start()
