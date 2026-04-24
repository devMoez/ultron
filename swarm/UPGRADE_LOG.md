# Swarm Upgrade Log

## 2026-04-24 – Initial creation

### Step 0 – Existing agent search
- Searched for `build.py`, `plan.py`, `build_agent.py`, `plan_agent.py` in `swarm/` and parent dirs.
- **Result: No existing agents found.**
- Action: Created minimal new implementations for both `planner.py` and `builder.py` from scratch.

### Files created
| File | Description |
|------|-------------|
| `swarm_config.py` | Shared ports, paths, constants |
| `setup_db.py` | SQLite schema init |
| `agents/base_agent.py` | BaseAgent with heartbeat, filelock, FastAPI routes |
| `agents/planner.py` | PlannerAgent (port 5005) |
| `agents/designer.py` | DesignerAgent (port 5001) |
| `agents/builder.py` | BuilderAgent (port 5002) |
| `agents/debugger.py` | DebuggerAgent (port 5003) – polls every 30s |
| `agents/verifier.py` | VerifierAgent (port 5004) – regression check |
| `orchestrator.py` | Main orchestrator (port 5000) |
| `start.ps1` | One-click PowerShell launcher |
| `requirements.txt` | Python deps |
| `README.md` | Usage docs |

### Architecture decisions
- All agents inherit `BaseAgent` with unified heartbeat, lock, and HTTP endpoints.
- Task queue via JSON files in `tasks/queue/` — no message broker needed.
- SQLite WAL mode for concurrent reads.
- File locks via `filelock` library, stale locks auto-cleaned by orchestrator after 30s.
- Git rollback only attempted when `.git` directory exists in project root.

### TUI status
- **Not implemented** per spec. Port 5006 reserved.
- When ready: use Textual library, poll `GET /status` every second.
