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
from filelock import FileLock, Timeout

SWARM_ROOT = Path(__file__).resolve().parent.parent
LOCKS_DIR  = SWARM_ROOT / "locks"
LOGS_DIR   = SWARM_ROOT / "logs"
MEMORY_DIR = SWARM_ROOT / "memory"
ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://127.0.0.1:5000")

LOCK_TIMEOUT   = 10   # seconds to wait for a file lock
HEARTBEAT_INTERVAL = 5  # seconds between heartbeats


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

    # ── Logging ──────────────────────────────────────────────────────────────

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            log_file = LOGS_DIR / f"{self.name}.log"
            fh = logging.FileHandler(log_file, encoding="utf-8")
            fh.setLevel(logging.DEBUG)
            ch = logging.StreamHandler(sys.stdout)
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
                if self._current_task:
                    raise HTTPException(status_code=409, detail="Agent is busy")
                self._current_task = task
            # Run in background thread so HTTP response is immediate
            threading.Thread(
                target=self._execute_task_safe,
                args=(task,),
                daemon=True,
            ).start()
            return {"accepted": True, "agent": self.name}

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
            with self._task_lock:
                self._current_task = None

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
