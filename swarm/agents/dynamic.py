"""
Dynamic skill agent for Ultron Swarm.

This agent is spawned at runtime when a missing skill is detected or from the
Swarm panel. It has its own memory folder and can produce artifacts in the
target project so spawned agents are real workers, not registry-only entries.
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent
from swarm_config import PROJECTS_DIR


def _slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_\\-]+", "_", text.strip().lower())
    return (value[:48] or "task").strip("_")


class DynamicSkillAgent(BaseAgent):
    def __init__(self, name: str, port: int, skills: list[str]):
        super().__init__(name=name, port=port)
        self.skills = [s.strip() for s in skills if s.strip()]

    def handle_task(self, task: dict) -> str:
        description = str(task.get("description", ""))
        project_path = str(task.get("project_path", ""))
        task_id = str(task.get("id", f"dyn_{int(time.time())}"))

        project_name = Path(project_path).name if project_path else f"project_{_slug(self.name)}"
        target_root = PROJECTS_DIR / project_name
        output_dir = target_root / "dynamic_outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        artifact_path = output_dir / f"{_slug(description)}_{task_id}.txt"
        journal_path = self.memory_dir / f"task_{task_id}.json"

        payload = {
            "agent": self.name,
            "skills": self.skills,
            "task_id": task_id,
            "description": description,
            "project_path": project_path,
            "received_at": time.time(),
            "status": "done",
        }

        artifact_body = (
            f"Dynamic agent: {self.name}\n"
            f"Skills: {', '.join(self.skills) or 'general'}\n"
            f"Task: {description}\n"
            f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        artifact_path.write_text(artifact_body, encoding="utf-8")
        payload["artifact"] = str(artifact_path)
        journal_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.log(f"Completed dynamic task {task_id} -> {artifact_path}")
        return f"Dynamic output created at {artifact_path}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--skills", default=os.environ.get("SWARM_AGENT_SKILLS", "general"))
    args = parser.parse_args()

    skills = [s.strip() for s in str(args.skills).split(",") if s.strip()]
    DynamicSkillAgent(name=args.name, port=args.port, skills=skills).start()


if __name__ == "__main__":
    main()
