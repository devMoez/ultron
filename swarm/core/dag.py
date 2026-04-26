"""
Shared Task DAG — every agent can read and write.
Tasks are nodes; dependencies are directed edges (A → B means B cannot start until A is DONE).

Thread-safe; designed to be used from both the orchestrator thread and agent threads.
"""
import threading
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    PENDING  = "pending"   # waiting on dependencies
    READY    = "ready"     # deps satisfied, not yet assigned
    ASSIGNED = "assigned"  # claimed by an agent, not yet running
    RUNNING  = "running"   # agent is actively working
    DONE     = "done"      # completed successfully
    FAILED   = "failed"    # exhausted retries


@dataclass
class DAGTask:
    id: str
    description: str
    required_skills: list[str]
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    retry_count: int = 0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "required_skills": self.required_skills,
            "status": self.status.value,
            "assigned_agent": self.assigned_agent,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "retry_count": self.retry_count,
            "metadata": self.metadata,
        }


class DAGManager:
    """
    Directed Acyclic Graph for task management.

    Usage:
        dag = DAGManager()
        t1 = dag.add_task("Research auth libraries", ["research"])
        t2 = dag.add_task("Build login endpoint",    ["code"])
        dag.add_dependency(t2.id, t1.id)   # t2 waits for t1
        ready = dag.get_ready_tasks()       # → [t1]
        dag.mark_done(t1.id, "Found: bcrypt, passlib")
        ready = dag.get_ready_tasks()       # → [t2]
    """

    MAX_RETRIES = 3

    def __init__(self):
        self._lock = threading.RLock()
        self._tasks:  dict[str, DAGTask]   = {}
        self._deps:   dict[str, set[str]]  = {}   # task_id → set of dependency ids
        self._rdeps:  dict[str, set[str]]  = {}   # task_id → tasks that depend on it
        self._events: list[dict]           = []

    # ── Public API ────────────────────────────────────────────────────────────

    def add_task(
        self,
        description: str,
        required_skills: list[str],
        task_id: str | None = None,
        metadata: dict | None = None,
    ) -> DAGTask:
        with self._lock:
            tid = task_id or str(uuid.uuid4())[:8]
            task = DAGTask(
                id=tid,
                description=description,
                required_skills=required_skills,
                metadata=metadata or {},
            )
            self._tasks[tid] = task
            self._deps[tid]  = set()
            self._rdeps.setdefault(tid, set())
            self._emit("task_added", tid, {"description": description[:80], "skills": required_skills})
            self._recompute(tid)
            return task

    def add_dependency(self, task_id: str, depends_on: str) -> None:
        """Make task_id wait until depends_on is DONE."""
        with self._lock:
            if task_id not in self._tasks or depends_on not in self._tasks:
                raise ValueError(f"Unknown task id: {task_id!r} or {depends_on!r}")
            self._deps[task_id].add(depends_on)
            self._rdeps.setdefault(depends_on, set()).add(task_id)
            self._recompute(task_id)
            self._emit("dep_added", task_id, {"depends_on": depends_on})

    def get_ready_tasks(self) -> list[DAGTask]:
        with self._lock:
            return [t for t in self._tasks.values() if t.status == TaskStatus.READY]

    def mark_assigned(self, task_id: str, agent_name: str) -> None:
        with self._lock:
            t = self._tasks.get(task_id)
            if t and t.status in (TaskStatus.READY, TaskStatus.PENDING):
                t.status = TaskStatus.ASSIGNED
                t.assigned_agent = agent_name
                t.started_at = time.time()
                self._emit("assigned", task_id, {"agent": agent_name})

    def mark_running(self, task_id: str) -> None:
        with self._lock:
            t = self._tasks.get(task_id)
            if t:
                t.status = TaskStatus.RUNNING

    def mark_done(self, task_id: str, result: str) -> None:
        with self._lock:
            t = self._tasks.get(task_id)
            if t:
                t.status = TaskStatus.DONE
                t.result = result
                t.completed_at = time.time()
                self._emit("done", task_id, {"result": result[:100]})
                for dep_id in self._rdeps.get(task_id, set()):
                    self._recompute(dep_id)

    def mark_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            t = self._tasks.get(task_id)
            if not t:
                return
            if t.retry_count < self.MAX_RETRIES:
                t.retry_count += 1
                t.status = TaskStatus.READY
                t.assigned_agent = None
                self._emit("retry", task_id, {"attempt": t.retry_count})
            else:
                t.status = TaskStatus.FAILED
                t.error = error
                t.completed_at = time.time()
                self._emit("failed", task_id, {"error": error[:100]})

    def get_all(self) -> list[dict]:
        with self._lock:
            return [t.to_dict() for t in self._tasks.values()]

    def get_edges(self) -> list[dict]:
        """Return DAG edges for visualization: [{"from": id, "to": id}]."""
        with self._lock:
            edges = []
            for tid, deps in self._deps.items():
                for dep in deps:
                    edges.append({"from": dep, "to": tid})
            return edges

    def get_events(self, since: float = 0.0) -> list[dict]:
        with self._lock:
            return [e for e in self._events if e["ts"] > since]

    # ── Internal ──────────────────────────────────────────────────────────────

    def _recompute(self, task_id: str) -> None:
        t = self._tasks.get(task_id)
        if not t or t.status in (TaskStatus.DONE, TaskStatus.FAILED,
                                  TaskStatus.RUNNING, TaskStatus.ASSIGNED):
            return
        deps_done = all(
            self._tasks.get(d, DAGTask("?", "", [])).status == TaskStatus.DONE
            for d in self._deps.get(task_id, set())
        )
        t.status = TaskStatus.READY if deps_done else TaskStatus.PENDING

    def _emit(self, event: str, task_id: str, data: dict) -> None:
        self._events.append({"ts": time.time(), "event": event, "task_id": task_id, **data})
        if len(self._events) > 500:
            self._events = self._events[-500:]


# Process-wide singleton shared by orchestrator + agents
shared_dag = DAGManager()
