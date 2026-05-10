# Claude Code — Constructive Programming Rules

## NO DUMMY/STUB IMPLEMENTATIONS
Never create TODO stubs, hardcoded mock data, or placeholder implementations. Write complete, working production code on first pass. Every function must do what it says.

## DEPENDENCY PROPAGATION
When changing any file: find ALL files that import/use/reference it → update every single one in the same session. Run blast radius analysis before touching anything. If a change breaks a dependent, fix it before moving on.

## FULL CONTEXT
Read all relevant files in the feature area before writing. Parse existing types, interfaces, patterns. Never assume state management or data flow. Use grep to find every usage of any function you modify.

## BACKEND→UI CONNECTION
Backend API changes require corresponding UI updates in the same change. UI must use real API calls, not mocks. State shapes must match actual backend responses. Forms must validate matching backend rules. Error handling must handle real backend errors.

## NO FAKE UI
No lorem ipsum. No static arrays where API data belongs. No fake loading states. Every button does a real action. Every form submits to a real endpoint. No "Coming Soon" unless explicitly requested.

## REAL BUSINESS LOGIC
Business logic in services/hooks, not components. API calls must have loading + error + retry handling. Data transformations must be type-safe. Event handlers must have proper cleanup + debouncing/throttling.

## FORBIDDEN PATTERNS
- `// TODO:` or `/* implement later */` — never
- Hardcoded test data in production code
- Empty catch blocks or silent failures
- `return data || []` or similar silent defaults
- `<div>Coming soon</div>` — never

## SELF-AUDIT
After every change, ask: Is this real production code? Did I break dependents? Does UI actually connect to backend here? Would this pass code review?

---

# Project-Specific: Cortex + Swarm + Ultron

## CORTEX (architectural awareness engine, C++17)
- **Dual-brain**: internal_brain (port 9090, research) + cortex.exe (port 8080, expansion)
- **Must call `cortex_preflight` before touching any file** — checks blast radius via Cortex's dependency analyzer
- **Must call `cortex_verify` after writing** — only done when passed:true
- **Cortex session start** → `cortex_summary` before any code
- C++ rules: RAII everywhere, no raw pointers, smart pointers only, const-correctness, nlohmann/json for state, httplib for networking
- **Cortex offline?** → `.\internal_brain\mind.exe C:\path\to\project` then `.\cortex.exe`

## SWARM (Python multi-agent, port 8000)
- FastAPI orchestrator with lifespan handlers. Agent scripts at `swarm/orchestrator.py`
- Agents: planner(5005), designer(5001), builder(5002), debugger(5003), verifier(5004)
- Always update `swarm/agent.py`, `swarm/blackboard.py`, `swarm/db.py`, `swarm/skill_library.py` in sync
- WebSocket bridge at `/ws`, UI at `/`
- When changing the swarm API, update both the FastAPI routes AND the UI JavaScript

## ULTRON (TypeScript/Bun core)
- Bun > Node. Effect.js, Solid.js. No semicolons, single quotes, 2-space indent
- Never suggest React unless asked
- Dark theme, minimal UI by default
- Telegram banned in Pakistan — use Discord

## MEMORY SYSTEM
- Session memory via MCP: `session_start` at begin, `session_end` at end
- `recall_memory` on demand. `remember` for explicit saves
- Memory files at `C:\Users\moezf\Desktop\opencode\memory\`
- Never load or mention memory files manually — let the MCP handle it

## CROSS-REPO: Cortex + Ultron
- Cortex and Ultron are separate repos (`devMoez/Cortex`, `devMoez/ultron`) but tightly coupled
- Changes to one often affect the other (e.g., Cortex MCP server updates affect Ultron's MCP config)
- When updating `opencode.jsonc` MCP entries, check both Cortex and Ultron paths
- `start-all.ps1` launches both — keep in sync

## PERFORMANCE BUDGET (keep Claude fast)
- Keep context tight: only read files you actually need for the task
- Prefer targeted grep over full-file reads
- Use separate rule files (this file) instead of bloating system prompt
- Don't repeat these rules in every response — they're already loaded