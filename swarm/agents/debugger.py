# This file handles LLM-assisted test failure analysis for the Ultron debugger agent.
"""
Debugger Agent — runs pytest, feeds failures to deepseek-chat for root-cause + fix.
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
from llm_router import quick
from rag.retriever import retrieve_and_format
from swarm_config import PROJECTS_DIR, ORCHESTRATOR_URL

POLL_INTERVAL = 30  # seconds between periodic sweeps


SYSTEM_PROMPT = """You are Ultron's Debugger. Analyse test failures and produce a minimal fix.

Given the test output and source code, return a JSON object:
{
  "root_cause": "One sentence explanation",
  "fix_description": "What to change",
  "fixed_code": "The complete corrected source file content"
}

Return ONLY valid JSON. No markdown fences."""


class DebuggerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="debugger", port=5003)
        self._debug_timer: threading.Timer | None = None

    def handle_task(self, task: dict) -> str:
        project_path = task.get("project_path", "")
        session_id   = task.get("session_id")
        return self._run_and_debug(project_path, session_id)

    # ── Periodic sweep ────────────────────────────────────────────────────────

    def _schedule_next(self) -> None:
        self._debug_timer = threading.Timer(POLL_INTERVAL, self._periodic_debug)
        self._debug_timer.daemon = True
        self._debug_timer.start()

    def _periodic_debug(self) -> None:
        for project_dir in PROJECTS_DIR.iterdir():
            if project_dir.is_dir():
                result = self._run_and_debug(str(project_dir), None)
                self.log(f"[periodic] {project_dir.name}: {result}")
        self._schedule_next()

    # ── Core logic ────────────────────────────────────────────────────────────

    def _run_and_debug(self, project_path: str, session_id: str | None) -> str:
        if not project_path:
            return "No project path provided"

        p = Path(project_path)
        if not p.exists():
            return f"Path does not exist: {project_path}"

        tests_dir = p / "tests"
        if not tests_dir.exists() or not any(tests_dir.glob("test_*.py")):
            return "No tests found"

        self.log(f"Running tests in {tests_dir}")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tests_dir), "-v", "--tb=short", "-q"],
            capture_output=True, text=True, timeout=120, cwd=str(p),
        )
        output = result.stdout + result.stderr

        if result.returncode == 0:
            self.log("All tests passed")
            return f"PASSED\n{output[:300]}"

        self.log("Tests failed — invoking LLM for root-cause analysis", "warning")

        # Collect failing source files for context
        src_snippet = self._collect_src(p, output)
        rag_context = retrieve_and_format(output[:500], k=3)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Test output:\n{output[:2000]}\n\n"
                f"Source code:\n{src_snippet}\n"
                + (f"\nRelevant codebase context:\n{rag_context}" if rag_context else "")
            )},
        ]

        try:
            import json
            raw = quick(messages, temperature=0.0)
            analysis = json.loads(raw)
            root_cause = analysis.get("root_cause", "Unknown")
            fix_desc   = analysis.get("fix_description", "")
            fixed_code = analysis.get("fixed_code", "")

            # Write fix back if we got real code
            if fixed_code and len(fixed_code) > 50:
                failed_file = self._find_failed_src(p, output)
                if failed_file:
                    failed_file.write_text(fixed_code, encoding="utf-8")
                    self.log(f"Applied LLM fix to {failed_file}")

            self._report_failure(project_path, output)
            return f"FAILED — {root_cause}. Fix: {fix_desc}"

        except Exception as exc:
            self.log(f"LLM analysis failed: {exc}", "warning")
            self._report_failure(project_path, output)
            return f"FAILED\n{output[:400]}"

    def _collect_src(self, project_dir: Path, test_output: str) -> str:
        """Read source files referenced in test output."""
        src_dir = project_dir / "src"
        if not src_dir.exists():
            return ""
        snippets = []
        for f in list(src_dir.glob("*.py"))[:3]:
            try:
                content = f.read_text(encoding="utf-8")
                snippets.append(f"# {f.name}\n{content[:1500]}")
            except Exception:
                pass
        return "\n\n".join(snippets)

    def _find_failed_src(self, project_dir: Path, output: str) -> Path | None:
        """Try to identify which source file caused the failure."""
        src_dir = project_dir / "src"
        if not src_dir.exists():
            return None
        for f in src_dir.glob("*.py"):
            if f.stem in output:
                return f
        files = list(src_dir.glob("*.py"))
        return files[0] if files else None

    def _report_failure(self, project_path: str, output: str) -> None:
        import httpx
        try:
            httpx.post(
                f"{ORCHESTRATOR_URL}/task_result",
                json={
                    "agent": self.name, "success": False,
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
