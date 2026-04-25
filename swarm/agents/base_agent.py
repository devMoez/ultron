"""
Step 3: BaseAgent – common class all swarm agents inherit from.
"""
import abc
import logging
import os
import sys
import threading
import time
from pathlib import Path

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
class Timeout(Exception):
    pass

class FileLock:
    def __init__(self, lock_file: str, timeout: int = 10):
        self.lock_file = lock_file
        self.timeout = timeout
        self._fh = None

    def acquire(self):
        import time
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                self._fh = open(self.lock_file, "x")
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise Timeout(f"Could not acquire lock: {self.lock_file}")
                time.sleep(0.05)

    def release(self):
        if self._fh:
            self._fh.close()
            self._fh = None
            try:
                os.unlink(self.lock_file)
            except Exception:
                pass

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        self.release()

SWARM_ROOT = Path(__file__).resolve().parent.parent
LOCKS_DIR  = SWARM_ROOT / "locks"
LOGS_DIR   = SWARM_ROOT / "logs"
MEMORY_DIR = SWARM_ROOT / "memory"
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://127.0.0.1:5000")

LOCK_TIMEOUT   = 10   # seconds to wait for a file lock
HEARTBEAT_INTERVAL = 5  # seconds between heartbeats

# Parallel-session feature flag (read locally so agents don't import swarm_config
# unconditionally — keeps existing single-task semantics on by default).
PARALLEL_SESSIONS = os.environ.get("SWARM_PARALLEL_SESSIONS", "0") == "1"
MAX_TASKS_PER_AGENT = int(os.environ.get("SWARM_MAX_TASKS_PER_AGENT", "5"))


class BaseAgent(abc.ABC):
    def __init__(self, name: str, port: int, orchestrator_url: str = ORCHESTRATOR_URL):
        self.name = name
        self.port = port
        self.orchestrator_url = orchestrator_url

        # Paths
        self.memory_dir = MEMORY_DIR / name
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        LOCKS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        # Logger
        self.logger = self._setup_logger()

        # FastAPI app
        self.app = FastAPI(title=f"Ultron {name.capitalize()} Agent")
        self._register_routes()

        # Heartbeat thread
        self._stop_event = threading.Event()
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, daemon=True, name=f"{name}-heartbeat"
        )

        # Current task storage (thread-safe via lock)
        self._task_lock = threading.Lock()
        self._current_task: dict | None = None

        # Parallel-session support (gated). When enabled, agents accept up to
        # MAX_TASKS_PER_AGENT concurrent tasks, keyed by task id. Existing
        # single-task semantics (current_task) is preserved when the flag is
        # off.
        self._active_tasks: dict[int, dict] = {}        # id → task
        self._cancelled_sessions: set[str] = set()
        # Pending amendments by session_id; agents inspect via check_amendment().
        self._pending_amendments: dict[str, list[dict]] = {}

    # ── Logging ──────────────────────────────────────────────────────────────

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            log_file = LOGS_DIR / f"{self.name}.log"
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            ch = logging.StreamHandler(sys.stderr)
            ch.setLevel(logging.INFO)
            fmt = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s")
            fh.setFormatter(fmt)
            ch.setFormatter(fmt)
            logger.addHandler(fh)
            logger.addHandler(ch)
        return logger

    def log(self, message: str, level: str = "info") -> None:
        getattr(self.logger, level, self.logger.info)(message)

    # ── File locking ──────────────────────────────────────────────────────────

    def acquire_lock(self, file_path: str) -> FileLock:
        lock_file = LOCKS_DIR / (Path(file_path).name + ".lock")
        lock = FileLock(str(lock_file), timeout=LOCK_TIMEOUT)
        try:
            lock.acquire()
            self.log(f"Lock acquired: {file_path}")
            return lock
        except Timeout:
            self.log(f"Could not acquire lock for {file_path} within {LOCK_TIMEOUT}s", "warning")
            raise

    def release_lock(self, lock: FileLock) -> None:
        lock.release()
        self.log(f"Lock released: {lock.lock_file}")

    # ── Heartbeat ─────────────────────────────────────────────────────────────

    def _heartbeat_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                with httpx.Client(timeout=3.0) as client:
                    client.post(f"{self.orchestrator_url}/heartbeat", json={
                        "agent": self.name,
                        "port":  self.port,
                        "pid":   os.getpid(),
                        "status": "busy" if self._current_task else "idle",
                    })
            except Exception:
                pass  # orchestrator may not be ready yet
            self._stop_event.wait(HEARTBEAT_INTERVAL)

    # ── HTTP routes ───────────────────────────────────────────────────────────

    def _register_routes(self) -> None:
        @self.app.get("/status")
        def status():
            with self._task_lock:
                task = self._current_task
            return {
                "agent":   self.name,
                "port":    self.port,
                "pid":     os.getpid(),
                "status":  "busy" if task else "idle",
                "task":    task,
            }

        @self.app.post("/assign_task")
        async def assign_task(task: dict):
            with self._task_lock:
                if PARALLEL_SESSIONS:
                    if len(self._active_tasks) >= MAX_TASKS_PER_AGENT:
                        raise HTTPException(
                            status_code=429,
                            detail=f"Agent at capacity ({MAX_TASKS_PER_AGENT})",
                        )
                    tid = task.get("id") or f"x{int(time.time()*1000)}"
                    self._active_tasks[tid] = task
                    if self._current_task is None:
                        self._current_task = task     # back-compat for /status
                else:
                    if self._current_task:
                        raise HTTPException(status_code=409, detail="Agent is busy")
                    self._current_task = task
            # Run in background thread so HTTP response is immediate
            threading.Thread(
                target=self._execute_task_safe,
                args=(task,),
                daemon=True,
            ).start()
            return {"accepted": True, "agent": self.name,
                    "concurrent": PARALLEL_SESSIONS}

        @self.app.post("/amend")
        async def amend(payload: dict):
            """Receive an amendment from the SessionManager. Stored for the
            agent's handle_task to consume via self.check_amendment(session_id)."""
            sid = (payload or {}).get("session_id")
            text = (payload or {}).get("text", "")
            mode = (payload or {}).get("mode", "")
            if not sid or not text:
                raise HTTPException(status_code=400, detail="session_id and text required")
            with self._task_lock:
                self._pending_amendments.setdefault(sid, []).append({
                    "text":         text,
                    "mode":         mode,
                    "submitted_at": payload.get("submitted_at") or time.time(),
                })
            self.log(f"Amendment received for session {sid}: {text[:80]}")
            return {"ok": True}

        @self.app.post("/cancel")
        async def cancel(payload: dict):
            sid = (payload or {}).get("session_id")
            if not sid:
                raise HTTPException(status_code=400, detail="session_id required")
            with self._task_lock:
                self._cancelled_sessions.add(sid)
            self.log(f"Cancel signal received for session {sid}", "warning")
            return {"ok": True}

        @self.app.get("/active")
        async def active():
            with self._task_lock:
                return {
                    "agent":        self.name,
                    "count":        len(self._active_tasks),
                    "max":          MAX_TASKS_PER_AGENT,
                    "task_ids":     list(self._active_tasks.keys()),
                    "amendments":   {k: len(v) for k, v in self._pending_amendments.items()},
                    "cancelled":    list(self._cancelled_sessions),
                }

        @self.app.post("/call/{agent_name}")
        async def call_agent(agent_name: str, payload: dict):
            """Proxy a call to another agent."""
            from swarm_config import AGENT_PORTS  # local import to avoid circular
            port = AGENT_PORTS.get(agent_name)
            if not port:
                raise HTTPException(status_code=404, detail=f"Unknown agent: {agent_name}")
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(
                        f"http://127.0.0.1:{port}/assign_task", json=payload
                    )
                return resp.json()
            except Exception as e:
                raise HTTPException(status_code=502, detail=str(e))

        @self.app.post("/report_status")
        async def report_status(payload: dict):
            """Receive a status report from another agent."""
            self.log(f"Status report received: {payload}")
            return {"ok": True}

    def _execute_task_safe(self, task: dict) -> None:
        try:
            result = self.handle_task(task)
            self._report_completion(task, result, success=True)
        except Exception as exc:
            self.log(f"Task failed: {exc}", "error")
            self._report_completion(task, str(exc), success=False)
        finally:
            tid = task.get("id")
            with self._task_lock:
                if tid is not None and tid in self._active_tasks:
                    self._active_tasks.pop(tid, None)
                # Pick another active task to expose via _current_task, or clear it.
                if not self._active_tasks:
                    self._current_task = None
                elif self._current_task is task:
                    self._current_task = next(iter(self._active_tasks.values()))

    # ── Helpers for handle_task implementations ──────────────────────────────

    def check_amendment(self, session_id: str | None) -> list[dict]:
        """Return any pending amendments for this session and clear them.
        Agents that support mid-task adjustment should call this between
        LLM steps. Agents that don't can just ignore it."""
        if not session_id:
            return []
        with self._task_lock:
            pending = self._pending_amendments.pop(session_id, [])
        return pending

    def is_session_cancelled(self, session_id: str | None) -> bool:
        if not session_id:
            return False
        with self._task_lock:
            return session_id in self._cancelled_sessions

    def _report_completion(self, task: dict, result: str, success: bool) -> None:
        try:
            with httpx.Client(timeout=5.0) as client:
                client.post(f"{self.orchestrator_url}/task_result", json={
                    "task_id": task.get("id"),
                    "agent":   self.name,
                    "success": success,
                    "result":  result,
                })
        except Exception as e:
            self.log(f"Could not report task result: {e}", "warning")

    # ── Abstract ──────────────────────────────────────────────────────────────

    @abc.abstractmethod
    def handle_task(self, task: dict) -> str:
        """Override in each agent. Return a result string."""

    # ── Startup ───────────────────────────────────────────────────────────────

    def start(self) -> None:
        self.log(f"Starting {self.name} agent on port {self.port}")
        self._heartbeat_thread.start()
        uvicorn.run(self.app, host="127.0.0.1", port=self.port, log_level="warning")
