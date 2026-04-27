# 🔄 Ultron Logic Flows

This file explains how the different parts of the system interact with each other.

## 1. Command Execution Flow (CLI)
1. User enters command via `ultron` CLI.
2. `packages/opencode/src/cli/` parses the input.
3. The **Engine** (`packages/opencode/src/agent/`) evaluates the intent.
4. If a tool is needed, `packages/opencode/src/tool/` is invoked.

## 2. Multi-Agent Tasking (Swarm)
1. Engine identifies a complex task.
2. A request is sent to the **Swarm Orchestrator** (`swarm/orchestrator.py`).
3. Swarm spawns specialized Python agents (Planner, Builder, Debugger).
4. Results are aggregated and returned to the Engine.

## 3. UI Updates (Dashboard)
1. **Ultron System** (`ultron-system/main.py`) runs as a background service.
2. It monitors logs and agent states.
3. The **Dashboard UI** (`ultron-system/ui/`) visualizes the swarm activity in real-time.

---

**AI Instruction:** Refer to this file to understand cross-package dependencies before modifying communication layers.
