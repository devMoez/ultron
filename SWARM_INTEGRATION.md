# 🐝 Ultron Swarm: Multi-Agent Orchestration

The Swarm is the tactical layer of Ultron. It enables a coordinated effort between multiple specialized AI agents, allowing them to solve complex problems in parallel.

---

## 🏗️ Architecture

The Swarm operates as a dedicated Python-based ecosystem located in the `swarm/` directory.

### The Hive Mind
- **`orchestrator.py`** – The central hub (FastAPI). It manages agent lifecycles, health checks, and task distribution.
- **`session_manager.py`** – Handles parallel session routing (NEW, EDIT, CLARIFY).
- **`router_llm.py`** – A specialized LLM classifier that directs incoming requests to the most capable agent.

### Specialized Agents
| Agent | Port | Responsibility |
|-------|------|----------------|
| **Planner** | `5005` | Deconstructs high-level goals into actionable sub-tasks. |
| **Designer**| `5001` | Focuses on UI/UX, styling, and visual structure. |
| **Builder** | `5002` | The primary engine for code generation and implementation. |
| **Debugger**| `5003` | Analyzes stack traces and fixes logic errors. |
| **Verifier**| `5004` | Runs tests and validates that requirements are met. |

---

## 🚀 Getting Started

### 1. Fire up the Swarm
The easiest way to start the entire hive is via the provided PowerShell script:

```powershell
cd swarm
.\start.ps1
```

Or, manually start the orchestrator:
```bash
python swarm/orchestrator.py
```

The orchestrator will wake up at **http://localhost:5000** and automatically spawn its subordinate agents.

---

## 🖥️ UI & Control

Ultron provides a dedicated **Swarm Dashboard** in the sidebar (look for the 🤖 icon).

- **Real-time Status**: Monitor agent health, heartbeats, and restart counts.
- **Task Tracking**: View the history of tasks, their current status (Queued/Running/Done), and results.
- **Manual Override**: Directly submit tasks to specific agents via the control panel.

### TUI Dashboard
For those who prefer the terminal, a Textual-based dashboard is available:
```powershell
.\swarm\swarm-tui.ps1
```

---

## 🔌 API & Integration

The Swarm is fully integrated into Ultron's MCP (Model Context Protocol) tools.

### Submitting via AI
You can tell Ultron: *"Ask the builder to implement a login form"* and it will use the `submit_task` tool internally.

### Direct HTTP Control
```bash
curl -X POST http://localhost:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"description": "Refactor the auth service", "target_agent": "builder"}'
```

---

## 📈 Advanced: Parallel Sessions

Enable high-concurrency mode by setting the `SWARM_PARALLEL_SESSIONS` environment variable. This allows Ultron to process up to 5 tasks simultaneously.

```powershell
$env:SWARM_PARALLEL_SESSIONS = "1"
python swarm/orchestrator.py
```
