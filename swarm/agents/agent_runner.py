"""
Swarm Agent Runner — unified agent process.
Each agent runs as a standalone HTTP server on its assigned port.
Handles task execution, heartbeats, and status reporting.
Run by the orchestrator: python agent_runner.py --name planner --port 5005
"""
import argparse
import json
import logging
import os
import sys
import time
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [agent] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
log = logging.getLogger("agent_runner")

ORCHESTRATOR_URL = os.environ.get("ORCHESTRATOR_URL", "http://127.0.0.1:8000")


class AgentHandler(BaseHTTPRequestHandler):
    """HTTP handler for agent endpoints."""

    agent_name = "unknown"
    agent_port = 0
    current_task = None

    def log_message(self, fmt, *args):
        log.info(f"{self.agent_name}: {fmt % args}")

    def _send_json(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "alive",
                "agent": self.agent_name,
                "task": self.current_task,
            })
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/assign_task":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length) if length else b"{}"
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._send_json(400, {"error": "invalid json"})
                return
            task_id = data.get("id", "?")
            description = data.get("description", "")
            log.info(f"Task [{task_id}] assigned: {description[:60]}")
            self.current_task = task_id
            # Execute task in background thread
            threading.Thread(target=self._execute_task, args=(data,), daemon=True).start()
            self._send_json(200, {"ok": True, "task_id": task_id, "agent": self.agent_name})
        else:
            self._send_json(404, {"error": "not found"})

    def _execute_task(self, data):
        """Execute a task and report result back to orchestrator."""
        task_id = data.get("id", "?")
        description = data.get("description", "")
        try:
            log.info(f"Executing task [{task_id}]: {description[:60]}")
            # Report progress back to orchestrator
            self._report_result(task_id, "running", "")
            time.sleep(2)  # Simulate work
            result = f"Task {task_id} completed by {self.agent_name}"
            self._report_result(task_id, "done", result)
            log.info(f"Task [{task_id}] completed")
        except Exception as e:
            log.error(f"Task [{task_id}] failed: {e}")
            self._report_result(task_id, "failed", str(e))
        finally:
            self.current_task = None

    def _report_result(self, task_id, status, result):
        try:
            success = status == "done"
            payload = json.dumps({
                "task_id": task_id,
                "agent": self.agent_name,
                "status": status,
                "success": success,
                "result": result,
            }).encode()
            req = urllib.request.Request(
                f"{ORCHESTRATOR_URL}/task_result",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            log.warning(f"Report result failed: {e}")

    def _heartbeat_loop(self):
        """Send heartbeat to orchestrator every few seconds."""
        while True:
            try:
                payload = json.dumps({
                    "agent": self.agent_name,
                    "status": "busy" if self.current_task else "idle",
                    "port": self.agent_port,
                    "pid": os.getpid(),
                }).encode()
                req = urllib.request.Request(
                    f"{ORCHESTRATOR_URL}/heartbeat",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                urllib.request.urlopen(req, timeout=3)
            except Exception as e:
                log.debug(f"Heartbeat failed: {e}")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="Swarm Agent Runner")
    parser.add_argument("--name", default=os.environ.get("AGENT_NAME", "agent"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("AGENT_PORT", "0")))
    args = parser.parse_args()

    AgentHandler.agent_name = args.name
    AgentHandler.agent_port = args.port

    port = args.port or 0
    server = HTTPServer(("127.0.0.1", port), AgentHandler)
    actual_port = server.server_address[1]
    log.info(f"Agent {args.name} listening on port {actual_port}")

    # Start heartbeat thread
    hb = threading.Thread(target=AgentHandler._heartbeat_loop, args=(AgentHandler,), daemon=True)
    hb.start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Shutting down")
        server.shutdown()


if __name__ == "__main__":
    main()
