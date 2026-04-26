"""
SkillOrchestra — routes DAG tasks to agents by skill overlap.

Runs as a background thread. Every poll interval:
  1. Fetch READY tasks from the DAG
  2. Find best idle agent in the registry
  3. Dispatch via HTTP to that agent's /assign_task endpoint
  4. If skill is missing, trigger dynamic spawning via Builder agent
"""
import logging
import threading
import time
from typing import Callable, Optional

import httpx

from .dag import DAGManager, DAGTask
from .agent_registry import AgentRegistry, AgentInfo
from .message_bus import MessageBus

log = logging.getLogger("skill_orchestra")


class SkillOrchestra:
    """
    Continuously polls the DAG for ready tasks and dispatches them.
    Parallel: multiple tasks dispatched in the same tick to different agents.
    """

    def __init__(
        self,
        dag:           DAGManager,
        registry:      AgentRegistry,
        bus:           MessageBus,
        spawn_skill_fn: Optional[Callable[[str], None]] = None,
        poll_interval:  float = 1.5,
    ):
        self._dag      = dag
        self._reg      = registry
        self._bus      = bus
        self._spawn    = spawn_skill_fn
        self._poll     = poll_interval
        self._stop     = threading.Event()
        self._thread   = threading.Thread(
            target=self._loop, daemon=True, name="skill-orchestra"
        )
        self._dispatching: set[str] = set()   # task ids currently being dispatched

    def start(self) -> None:
        self._thread.start()
        log.info("SkillOrchestra running")

    def stop(self) -> None:
        self._stop.set()

    # ── Main loop ─────────────────────────────────────────────────────────────

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self._tick()
            except Exception as e:
                log.error(f"SkillOrchestra tick error: {e}")
            self._stop.wait(self._poll)

    def _tick(self) -> None:
        ready = self._dag.get_ready_tasks()
        for task in ready:
            if task.id in self._dispatching:
                continue   # already being dispatched
            agent = self._reg.best_for(task.required_skills)
            if agent:
                self._dispatching.add(task.id)
                self._dag.mark_assigned(task.id, agent.name)
                self._reg.mark_busy(agent.name, task.description)
                self._bus.publish(f"skill.{(task.required_skills or ['any'])[0]}", {
                    "event":       "task_dispatched",
                    "task_id":     task.id,
                    "agent":       agent.name,
                    "description": task.description[:80],
                })
                # Dispatch in a thread so the tick loop isn't blocked
                t = threading.Thread(
                    target=self._dispatch,
                    args=(task, agent),
                    daemon=True,
                )
                t.start()
            else:
                # Check for missing skills → spawn
                missing = self._reg.missing_skills(task.required_skills)
                if missing and self._spawn:
                    for skill in missing:
                        log.info(f"Spawning agent for missing skill: {skill!r}")
                        try:
                            self._spawn(skill)
                        except Exception as e:
                            log.error(f"Spawn failed for {skill!r}: {e}")

    def _dispatch(self, task: DAGTask, agent: AgentInfo) -> None:
        try:
            resp = httpx.post(
                f"http://127.0.0.1:{agent.port}/assign_task",
                json={
                    "id":          int(task.id) if task.id.isdigit() else task.id,
                    "description": task.description,
                    "required_skills": task.required_skills,
                    "metadata":    task.metadata,
                },
                timeout=10.0,
            )
            if resp.status_code != 200:
                raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:100]}")
            self._dag.mark_running(task.id)
            log.info(f"Task {task.id} dispatched to {agent.name}")
        except Exception as e:
            log.error(f"Dispatch error for task {task.id} → {agent.name}: {e}")
            self._dag.mark_failed(task.id, str(e))
            self._reg.mark_idle(agent.name)
        finally:
            self._dispatching.discard(task.id)
