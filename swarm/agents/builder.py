# This file handles LLM-driven code generation for the Ultron builder agent.
"""
Builder Agent — uses deepseek-chat (quick tier) + RAG to generate real code.
Port: 5002
"""
import sys
import uuid
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent
from llm_router import quick
from rag.retriever import retrieve_and_format
from swarm_config import PROJECTS_DIR


SYSTEM_PROMPT = """You are Ultron's Builder. You write clean, production-ready Python code.
Rules:
- Return ONLY the raw Python file content. No markdown fences, no explanation.
- Include a module docstring at the top.
- Include a main() function and if __name__ == '__main__': main() block.
- Use type hints. Handle errors gracefully.
- Write real, working implementation — never leave TODOs or NotImplementedError."""

TEST_SYSTEM_PROMPT = """You are Ultron's Builder writing pytest tests.
Rules:
- Return ONLY the raw Python test file. No markdown fences, no explanation.
- Import the module under test correctly.
- Write at least 3 meaningful test functions.
- Each test must have a docstring."""


class BuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="builder", port=5002)

    def handle_task(self, task: dict) -> str:
        description  = task.get("description", "")
        project_path = task.get("project_path", "")
        session_id   = task.get("session_id")
        self.log(f"Build task: {description}")

        project_name = Path(project_path).name if project_path else f"project_{uuid.uuid4().hex[:6]}"
        src_dir   = PROJECTS_DIR / project_name / "src"
        tests_dir = PROJECTS_DIR / project_name / "tests"
        src_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        slug     = description.lower().replace(" ", "_")[:40]
        src_file = src_dir / f"{slug}.py"

        # RAG: get relevant code snippets
        rag_context = retrieve_and_format(description, k=5)

        # Generate implementation
        impl_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Task: {description}\n"
                f"Module name: {slug}\n"
                + (f"\n{rag_context}" if rag_context else "")
            )},
        ]

        lock = self.acquire_lock(str(src_file))
        try:
            src_content = quick(impl_messages, temperature=0.1)
            src_file.write_text(src_content, encoding="utf-8")
            self.log(f"Wrote source: {src_file}")

            # Check for amendments mid-task
            amendments = self.check_amendment(session_id)
            if amendments:
                amended = self._apply_amendments(src_content, amendments, description)
                src_file.write_text(amended, encoding="utf-8")
                self.log(f"Applied {len(amendments)} amendment(s)")

            # Generate tests
            test_file = tests_dir / f"test_{slug}.py"
            if not test_file.exists():
                test_messages = [
                    {"role": "system", "content": TEST_SYSTEM_PROMPT},
                    {"role": "user",   "content": (
                        f"Write pytest tests for this module:\n\n{src_content}"
                    )},
                ]
                test_content = quick(test_messages)
                test_file.write_text(test_content, encoding="utf-8")
                self.log(f"Wrote tests: {test_file}")
        finally:
            self.release_lock(lock)

        if not self.is_session_cancelled(session_id):
            self._notify_verifier(project_path or str(PROJECTS_DIR / project_name))

        return f"Source created at {src_file}"

    def _apply_amendments(self, original: str, amendments: list[dict], description: str) -> str:
        """Re-generate the file incorporating amendment instructions."""
        amendment_text = "\n".join(f"- {a['text']}" for a in amendments)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Original task: {description}\n"
                f"Apply these amendments to the code below:\n{amendment_text}\n\n"
                f"Original code:\n{original}"
            )},
        ]
        return quick(messages, temperature=0.0)

    def _notify_verifier(self, project_path: str) -> None:
        import httpx
        from swarm_config import AGENT_PORTS
        try:
            httpx.post(
                f"http://127.0.0.1:{AGENT_PORTS['verifier']}/assign_task",
                json={"description": "Run tests after build change", "project_path": project_path},
                timeout=5.0,
            )
        except Exception as e:
            self.log(f"Could not notify verifier: {e}", "warning")


if __name__ == "__main__":
    BuilderAgent().start()
