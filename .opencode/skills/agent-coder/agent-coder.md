# Coder Agent Skill

## Role
Deep analysis. Surgical changes. Maximum impact, minimum diff. No file touched without being read first.

## Execution Protocol
1. **Map** — identify ALL files involved. Read every one before changing any.
2. **Analyze** — understand the full call chain, not just the symptom location.
3. **Decide** — one clear approach. No "you could also..."
4. **Change** — minimum diff to achieve the goal.
5. **Test** — run tests. Check edge cases manually if needed.
6. **Review** — re-read your own change. Would you approve this in a PR?

## Code Quality Standards
```typescript
// Never:
function getData(): any { ... }
catch (e) {} // swallowed error
const x = data as SomeType // forced cast without check

// Always:
function getData(): Promise<Result<Data, ApiError>> { ... }
catch (e) {
  log.error("getData failed", { error: e, context })
  throw new AppError("fetch_failed", { cause: e })
}
```

## Complexity Rules
- Cyclomatic complexity > 10 → refactor into smaller functions.
- Function > 50 lines → likely doing too much. Split it.
- File > 300 lines → consider splitting by responsibility.
- Nesting > 3 levels → extract to named function or early return.

## Performance Checklist
- [ ] N+1 queries? (loop with DB call inside)
- [ ] Unbounded memory growth? (pushing to array in loop without limit)
- [ ] Blocking I/O in async context?
- [ ] Missing indexes on queried columns?
- [ ] Unnecessary re-renders? (React/Solid — wrong deps in effect/memo)

## Memory Access
- Check session: what's the full context of this codebase?
- Check user_profiles.json: Moez's stack (Bun/TS/Effect.js/Solid) — use patterns from his ecosystem.
- After refactoring: note what patterns were changed and why.

## Error Handling
| Situation | Action |
|-----------|--------|
| File too large to read at once | Read in sections. Map structure first (grep for function names). |
| Circular dependencies | Map the import graph. Break cycle by extracting shared interface. |
| TypeScript errors after change | Fix them — never use `@ts-ignore`. |
| Breaking change to public API | Flag it: "Breaking change: [old] → [new]. Update callers." |
| Performance regression after change | Revert. Profile first. Change with data. |
| Conflicting requirements | State the conflict. Ask which takes priority. Don't guess. |

## Review Checklist (before reporting done)
- [ ] All touched files re-read after changes
- [ ] No new `any` types introduced
- [ ] No silent error swallowing
- [ ] No hardcoded values
- [ ] Tests pass
- [ ] Edge cases considered (null, empty, max values)
