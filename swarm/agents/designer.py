# This file handles LLM-driven UI generation for the Ultron designer agent.
"""
Designer Agent — uses deepseek-chat (quick tier) + RAG to generate real HTML/CSS/JS.
Port: 5001
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


SYSTEM_PROMPT = """You are Ultron's Designer. You write production-quality HTML/CSS/JS.
Rules:
- Return ONLY the raw HTML file. No markdown fences, no explanation.
- Single-file output: inline CSS in <style> and JS in <script>.
- Dark theme: background #0f0f0f, accent #7c3aed (Ultron purple).
- Fully functional: forms submit, buttons work, lists populate.
- Mobile-responsive with CSS Grid or Flexbox.
- No external CDN dependencies — use vanilla CSS/JS only."""


class DesignerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="designer", port=5001)

    def handle_task(self, task: dict) -> str:
        description  = task.get("description", "")
        project_path = task.get("project_path", "")
        session_id   = task.get("session_id")
        self.log(f"Design task: {description}")

        project_name = Path(project_path).name if project_path else f"project_{uuid.uuid4().hex[:6]}"
        design_dir   = PROJECTS_DIR / project_name / "design"
        design_dir.mkdir(parents=True, exist_ok=True)

        slug      = description.lower().replace(" ", "_")[:40]
        html_file = design_dir / f"{slug}.html"

        # RAG: look for relevant UI patterns
        rag_context = retrieve_and_format(description + " html css component", k=3)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Design task: {description}\n"
                + (f"\nReference patterns:\n{rag_context}" if rag_context else "")
            )},
        ]

        lock = self.acquire_lock(str(html_file))
        try:
            html_content = quick(messages, temperature=0.3)
            html_file.write_text(html_content, encoding="utf-8")
            self.log(f"Wrote design: {html_file}")

            # Apply any mid-task amendments
            amendments = self.check_amendment(session_id)
            if amendments:
                amended = self._apply_amendments(html_content, amendments, description)
                html_file.write_text(amended, encoding="utf-8")
                self.log(f"Applied {len(amendments)} amendment(s)")
        finally:
            self.release_lock(lock)

        if not self.is_session_cancelled(session_id):
            self._notify_verifier(project_path or str(PROJECTS_DIR / project_name))

        return f"Design created at {html_file}"

    def _apply_amendments(self, original: str, amendments: list[dict], description: str) -> str:
        amendment_text = "\n".join(f"- {a['text']}" for a in amendments)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Original task: {description}\n"
                f"Apply these amendments:\n{amendment_text}\n\n"
                f"Original HTML:\n{original}"
            )},
        ]
        return quick(messages, temperature=0.1)

    def _notify_verifier(self, project_path: str) -> None:
        import httpx
        from swarm_config import AGENT_PORTS
        try:
            httpx.post(
                f"http://127.0.0.1:{AGENT_PORTS['verifier']}/assign_task",
                json={"description": "Run tests after design change", "project_path": project_path},
                timeout=5.0,
            )
        except Exception as e:
            self.log(f"Could not notify verifier: {e}", "warning")


if __name__ == "__main__":
    DesignerAgent().start()
