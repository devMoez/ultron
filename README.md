# Ultron

> AI coding companion with a swarm brain. Built on OpenCode.

Zero-fluff assistant that owns your terminal, manages your projects, and parallelizes work across a team of specialist agents. Deep Windows integration. Memory that actually persists. No subscription nonsense.

---

## What it does

- **Swarm Orchestration** — Fire up a multi-agent crew (planner, builder, debugger, verifier, designer) that decomposes tasks, codes in parallel, and reports back. You talk to one agent; it talks to the rest.
- **Windows-native** — Desktop control, file management, screenshots, browser automation via Playwright. Not a Linux port with awkward hacks.
- **Persistent memory** — Remembers your coding style, project preferences, past decisions. Not a chat log — actual learned context across sessions.
- **Persona engine** — Swap between `beast` (raw speed), `codex` (architecture deep-dives), `trinity` (full-stack logic). Each with its own instructions and memory.
- **Terminal UI** — Full TUI mode for when you want to live in the terminal. Web UI for when you don’t.

---

## Quick start

```bash
git clone https://github.com/devMoez/ultron.git
cd ultron
bun install && bun build && bun link
```

Then from anywhere:

```bash
ultron           # Interactive command center
ultron --chat    # Quick chat mode
ultron tui       # Terminal UI
```

---

## The Swarm

This is where it gets interesting. The swarm is a Python-based multi-agent orchestrator on **port 8000** with a real-time web UI.

### One command to start

```powershell
swarm
```

That is it. From any terminal. First time? Run the setup once:

```powershell
.\setup-swarm-global.ps1
```

This adds the project root to your PATH so `swarm` is always available — PowerShell profile and Windows user PATH, both covered.

### What starts

| Component | What it does |
|-----------|-------------|
| **FastAPI orchestrator** | Manages agent lifecycle, task queue, health monitoring, WebSocket push |
| **Planner** | Decomposes complex requests into subtasks |
| **Designer** | Generates UI/UX specs and mockups |
| **Builder** | Writes code, spawns sub-agents, executes builds |
| **Debugger** | Fixes regressions, runs tests |
| **Verifier** | Validates output against requirements |
| **Web UI** | Single-page app at `http://localhost:8000` — no build step, no framework |

### Architecture

```
terminal                  orchestrator:8000              agents
─────────                ─────────────────             ───────
  swarm        ──HTTP──>  FastAPI lifespan              planner   :5005
   (cmd/ps1)              ├── / (UI)                     designer  :5001
                          ├── /ws (realtime)             builder   :5002
                          ├── /status                    debugger  :5003
                          ├── /submit                    verifier  :5004
                          ├── /heartbeat                 └── each subprocess
                          ├── /task_result
                          ├── /agents/spawn
                          ├── /dag/*
                          └── /snapshot
```

Each agent runs as an independent Python subprocess. The orchestrator watches heartbeats, restarts failures, queues tasks, and routes work by skill. The DAG system parallelizes where it can. WebSocket pushes state to every connected client in real time.

---

## Project layout

```
ultron/
├── packages/opencode/        # Core engine (TypeScript)
├── swarm/                    # Python swarm system
│   ├── orchestrator.py       # FastAPI app, lifespan, routes
│   ├── agent.py              # Agent process handler
│   ├── blackboard.py         # Shared state between agents
│   ├── db.py                 # SQLite persistence
│   ├── skill_library.py      # Skill/task registry
│   ├── ui/index.html         # Single-page Web UI (75 KB, zero deps)
│   └── logs/                 # Orchestrator + agent logs
├── .opencode/agent/          # Persona definitions
├── memory/                   # Persistent memory store
├── swarm.ps1                 # Global launcher (PowerShell)
├── swarm.cmd                 # Global launcher (cmd.exe)
└── setup-swarm-global.ps1    # One-time PATH setup
```

---

## Swarm API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serves the web UI |
| `/status` | GET | Agent status, recent tasks, sessions |
| `/submit` | POST | Submit a task for assignment |
| `/agents/spawn` | POST | Spawn a new agent with skills |
| `/agents/{name}/kill` | POST | Kill a running agent |
| `/agents/{name}/assign` | POST | Force-assign a task to an agent |
| `/dag` | GET | Current task DAG state |
| `/dag/submit` | POST | Submit a DAG-shaped workflow |
| `/route` | POST | Route a prompt to the best-fit agent |
| `/registry` | GET | Agent registry snapshot |
| `/sessions` | GET | Active session list |
| `/ws` | WebSocket | Real-time event stream |

---

## Requirements

- **Windows** (primary — some features are Win32-specific)
- **Python 3.10+** (for the swarm)
- **Bun** (for the core engine)
- **Node.js** (for Ultron TUI)

---

## Disclaimer

Built for my workflow. Might work for yours. No warranties, no telemetry, no subscriptions.

[@devMoez](https://github.com/devMoez)
