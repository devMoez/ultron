# Ultron Swarm

Multi-agent swarm that runs alongside Ultron. No OpenCode files were modified.

## Start

```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

First run auto-creates a venv and installs dependencies.

## Submit a task

Drop a JSON file into `tasks/queue/`:

```json
{
  "target_agent": "planner",
  "description": "build a login page with email and password",
  "project_path": "C:/Users/moezf/Desktop/opencode/swarm/projects/my_app"
}
```

**target_agent options:** `planner`, `designer`, `builder`, `debugger`, `verifier`

The planner automatically breaks big tasks into subtasks and routes them to the right agents.

## Ports

| Agent        | Port |
|--------------|------|
| Orchestrator | 5000 |
| Designer     | 5001 |
| Builder      | 5002 |
| Debugger     | 5003 |
| Verifier     | 5004 |
| Planner      | 5005 |

## Check status

```
GET http://127.0.0.1:5000/status
```

Returns all agent states + recent tasks.

## Check logs

```
swarm\logs\orchestrator.log
swarm\logs\planner.log
swarm\logs\builder.log
... etc
```

## Stop

Close the terminal that ran `start.ps1`, or:

```powershell
Get-Process python | Where-Object { $_.MainWindowTitle -like "*swarm*" } | Stop-Process
```

## Folder structure

```
swarm/
├── start.ps1           ← run this
├── orchestrator.py
├── swarm_config.py
├── setup_db.py
├── requirements.txt
├── agents/
│   ├── base_agent.py
│   ├── planner.py      port 5005
│   ├── designer.py     port 5001
│   ├── builder.py      port 5002
│   ├── debugger.py     port 5003
│   └── verifier.py     port 5004
├── memory/
│   ├── shared/state.sqlite
│   └── <agent_name>/
├── tasks/
│   ├── queue/          ← drop JSON tasks here
│   └── processing/
├── projects/           ← agent output goes here
└── logs/
```

## Resume in Claude

Say: **"check task memory swarm"** and Claude will read the progress file and continue.
