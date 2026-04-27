# This file handles high-level task decomposition for the Ultron swarm planner agent.
"""
Planner Agent — uses deepseek-r1 (reasoning tier) to decompose goals into typed subtasks.
Port: 5005
"""
import json
import sys
import time
import uuid
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

SWARM_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SWARM_ROOT))

from agents.base_agent import BaseAgent
from llm_router import reason
from rag.retriever import retrieve_and_format


# ── Schema ────────────────────────────────────────────────────────────────────

class TaskStep(BaseModel):
    target_agent: Literal["builder", "designer", "debugger", "verifier"]
    description: str
    expected_output: str
    depends_on: list[int] = []   # 0-based indices of steps this depends on


class Plan(BaseModel):
    goal_summary: str
    steps: list[TaskStep]


SYSTEM_PROMPT = """You are Ultron's Planner. Break the user's goal into concrete, ordered subtasks.
Each step must be assigned to exactly one agent:
- builder:  backend code, APIs, data models, scripts
- designer: HTML/CSS/JS UI, frontend components
- debugger: test execution, error analysis, bug investigation
- verifier: regression checks, validation, approval gates

Return a valid JSON object matching the Plan schema. Be precise. No fluff."""


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="planner", port=5005)

    def handle_task(self, task: dict) -> str:
        description  = task.get("description", "")
        project_path = task.get("project_path", "")
        session_id   = task.get("session_id")
        self.log(f"Planning task: {description}")

        # Inject relevant code context
        rag_context = retrieve_and_format(description, k=5)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": (
                f"Goal: {description}\n"
                f"Project path: {project_path or 'not specified'}\n\n"
                + (f"{rag_context}\n" if rag_context else "")
            )},
        ]

        try:
            plan = _call_with_retry(messages)
        except Exception as exc:
            self.log(f"LLM planning failed, using keyword fallback: {exc}", "warning")
            plan = self._keyword_fallback(description, project_path)

        self.log(f"Plan: {plan.goal_summary} → {len(plan.steps)} steps")

        queue_dir = SWARM_ROOT / "tasks" / "queue"
        queue_dir.mkdir(parents=True, exist_ok=True)

        subtasks = []
        for step in plan.steps:
            sub = {
                "description":    step.description,
                "target_agent":   step.target_agent,
                "expected_output": step.expected_output,
                "project_path":   project_path,
                "session_id":     session_id,
            }
            subtasks.append(sub)
            filename = f"task_{uuid.uuid4().hex[:8]}.json"
            (queue_dir / filename).write_text(json.dumps(sub, indent=2), encoding="utf-8")
            self.log(f"Queued → {step.target_agent}: {step.description}")
            time.sleep(0.05)

            if self.is_session_cancelled(session_id):
                self.log("Session cancelled during planning", "warning")
                break

        # Persist plan to memory
        plan_file = self.memory_dir / f"plan_{uuid.uuid4().hex[:6]}.json"
        plan_file.write_text(json.dumps({
            "original":   description,
            "summary":    plan.goal_summary,
            "subtasks":   subtasks,
            "created_at": time.time(),
        }, indent=2), encoding="utf-8")

        return f"Plan '{plan.goal_summary}' created with {len(plan.steps)} steps"

    def _keyword_fallback(self, description: str, project_path: str) -> Plan:
        """Original keyword-based fallback — used if LLM is unavailable."""
        desc_lower = description.lower()
        steps: list[TaskStep] = []

        if any(w in desc_lower for w in ["page", "ui", "design", "html", "css", "frontend", "component"]):
            steps.append(TaskStep(
                target_agent="designer",
                description=f"Design UI for: {description}",
                expected_output="HTML/CSS component files",
            ))
        if any(w in desc_lower for w in ["api", "backend", "server", "database", "model", "endpoint", "logic"]):
            steps.append(TaskStep(
                target_agent="builder",
                description=f"Implement backend for: {description}",
                expected_output="Python module with implementation",
            ))
        if any(w in desc_lower for w in ["test", "verify", "check", "validate"]):
            steps.append(TaskStep(
                target_agent="verifier",
                description=f"Verify tests for: {description}",
                expected_output="Test pass/fail report",
            ))
        if not steps:
            steps.append(TaskStep(
                target_agent="builder",
                description=description,
                expected_output="Implementation",
            ))

        return Plan(goal_summary=description, steps=steps)


def _call_with_retry(messages: list[dict], retries: int = 2) -> Plan:
    last_exc = None
    for attempt in range(retries + 1):
        try:
            raw = reason(messages, response_format=Plan)
            if isinstance(raw, str):
                return Plan.model_validate_json(raw)
            return raw  # type: ignore
        except Exception as exc:
            last_exc = exc
            time.sleep(1)
    raise last_exc  # type: ignore


if __name__ == "__main__":
    PlannerAgent().start()
