"""
Step 5: Planner Agent – breaks high-level tasks into subtasks and queues them.
Port: 5005
"""
import json
import sys
import time
import uuid
from pathlib import Path

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="planner", port=5005)

    def handle_task(self, task: dict) -> str:
        description = task.get("description", "")
        project_path = task.get("project_path", "")
        self.log(f"Planning task: {description}")

        # Break description into subtasks
        subtasks = self._decompose(description, project_path)
        self.log(f"Generated {len(subtasks)} subtasks")

        queue_dir = SWARM_ROOT / "tasks" / "queue"
        queue_dir.mkdir(parents=True, exist_ok=True)

        for sub in subtasks:
            filename = f"task_{uuid.uuid4().hex[:8]}.json"
            (queue_dir / filename).write_text(
                json.dumps(sub, indent=2), encoding="utf-8"
            )
            self.log(f"Queued subtask → {sub['target_agent']}: {sub['description']}")
            time.sleep(0.1)  # avoid collision on timestamp-based filenames

        # Save plan to memory
        plan_file = self.memory_dir / f"plan_{uuid.uuid4().hex[:6]}.json"
        plan_file.write_text(json.dumps({
            "original": description,
            "subtasks": subtasks,
            "created_at": time.time(),
        }, indent=2), encoding="utf-8")

        return f"Plan created with {len(subtasks)} subtasks"

    def _decompose(self, description: str, project_path: str) -> list[dict]:
        """
        Simple keyword-based decomposition.
        A real implementation would call an LLM here.
        """
        desc_lower = description.lower()
        subtasks: list[dict] = []
        base = {"project_path": project_path}

        # UI / design keywords
        if any(w in desc_lower for w in ["page", "ui", "design", "html", "css", "frontend", "component"]):
            subtasks.append({**base,
                "target_agent": "designer",
                "description": f"Design UI for: {description}",
            })

        # Backend / API keywords
        if any(w in desc_lower for w in ["api", "backend", "server", "database", "model", "endpoint", "logic"]):
            subtasks.append({**base,
                "target_agent": "builder",
                "description": f"Implement backend for: {description}",
            })

        # Test keywords
        if any(w in desc_lower for w in ["test", "verify", "check", "validate"]):
            subtasks.append({**base,
                "target_agent": "verifier",
                "description": f"Verify tests for: {description}",
            })

        # Default: send to builder if nothing matched
        if not subtasks:
            subtasks.append({**base,
                "target_agent": "builder",
                "description": description,
            })

        return subtasks


if __name__ == "__main__":
    PlannerAgent().start()
