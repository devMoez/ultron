# Ultron — Constructive Programming Rules

These rules are loaded as instructions for every session. They are not optional. Follow them strictly.

---

## NO DUMMY/STUB CODE

Never create TODO stubs, placeholder functions, hardcoded mock data, or "implement later" comments. Every function you write must do what it says, handle errors, and be production-ready on first pass. If you cannot implement something fully, say so — do not stub.

**Forbidden:**
- `// TODO: implement later`
- `function foo() { /* not implemented */ }`
- Hardcoded test data in production paths
- Empty catch blocks or silent failures (`catch(e) {}`)
- `return data || []` or similar silent defaults
- `if (condition) { /* no-op */ } else { ... }`
- `<div>Coming soon</div>` or equivalent in any language

---

## DEPENDENCY PROPAGATION (mandatory)

When changing ANY file you MUST:

1. Identify all files that import, reference, or depend on it
2. Update every single dependent file in the same session
3. Run cascade impact analysis before starting
4. If a change breaks a dependent, fix it before moving on

**Impact levels:**

| Change Type | Must Update |
|-------------|-------------|
| Interface/type change | ALL files importing it |
| Function signature | ALL call sites |
| API endpoint | ALL UI components + types + tests |
| State shape | ALL reducers, selectors, consumers |
| Environment variable | ALL config files + docs |
| DB schema | ALL repositories, queries, migrations |

---

## BACKEND → UI CONNECTION

- Backend API changes require corresponding UI updates in the same change
- UI must use real API calls — never mock services in production
- State shapes must match actual backend response shapes
- Form validation must mirror backend validation rules
- Error handling must handle real backend error responses (not just `console.log`)

---

## NO FAKE UI

- No lorem ipsum, placeholder text, or hardcoded sample data in production
- No static arrays where data should come from an API
- No fake loading states — every spinner must back a real async operation
- Every button, form, and interaction must perform a real action against a real endpoint
- No "Coming Soon" features unless explicitly requested by the user

---

## REAL BUSINESS LOGIC

- Business logic belongs in services/hooks/utilities, not in components or views
- All async operations must have: loading state, error state, retry mechanism
- Data transformations must preserve type safety at every step
- Side effects must have proper cleanup (abort controllers, unsubscribe, disposers)
- Event handlers must have proper debouncing/throttling where appropriate

---

## SELF-AUDIT (after every change)

Before marking any task complete, ask yourself:

- "Is this real production code or is it a stub?"
- "Did I break any dependent files?"
- "Does the UI actually connect to the backend here?"
- "Would this pass code review?"
- "Did I handle the error cases?"
- "Are there tests for the new logic?"

---

## PROJECT-SPECIFIC RULES

### Ultron Core (TypeScript/Bun)
- Bun runtime, not Node. Effect.js, Solid.js. No semicolons, single quotes, 2-space indent
- Dark theme, minimal UI. Never suggest React unless specifically asked
- Never ask "should I proceed?" — just execute

### Swarm (Python multi-agent, port 8000)
- FastAPI orchestrator at `swarm/orchestrator.py` with lifespan handlers
- Agent modules: `swarm/agent.py`, `swarm/blackboard.py`, `swarm/db.py`, `swarm/skill_library.py`
- Agents run on ports: planner(5005), designer(5001), builder(5002), debugger(5003), verifier(5004)
- API bridge at `/api/*` routes for the frontend UI
- When changing the API, update both the FastAPI route AND the UI JavaScript

### Cortex (architectural engine, C++17, separate repo)
- Dual-brain: `internal_brain/mind.exe` (port 9090) + `cortex.exe` (port 8080)
- C++ rules: RAII everywhere, smart pointers, const-correctness, nlohmann/json, httplib
- Must call cortex_preflight before touching files, cortex_verify after writing
- Cortex and Ultron are separate repos but tightly coupled via MCP config

### Memory System
- Session memory via MCP: `session_start` at begin, `session_end` at end
- `recall_memory` on demand. `remember` for explicit saves
- Never load or manipulate memory files manually — let the MCP handle it

---

## PERFORMANCE

- Keep context tight: only read files you actually need for the task
- Prefer targeted grep over full-file reads when looking for specific patterns
- Don't repeat these rules in every response — they are already loaded
