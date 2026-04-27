# 🛠️ Ultron Tech Stack & Standards

## 🚀 Runtimes & Environments
- **TypeScript:** Powered by [Bun](https://bun.sh/). Use `bun install` and `bun run`.
- **Python:** Version 3.10+. Managed via `venv` in the `swarm/` directory.
- **Node.js:** Compatibility layer for specific legacy scripts.

## 🏗️ Architecture
- **Monorepo:** Managed via **Turborepo** (`turbo.json`).
- **Frontend:** React + Vite + Vanilla CSS.
- **ORM:** Prisma (for persistent memory/local DB).
- **Communication:** MCP (Model Context Protocol) for tool integration.

## 📏 Coding Standards
1. **Type Safety:** Strict TypeScript everywhere. No `any` unless absolutely necessary.
2. **Functional Pattern:** Prefer composition over inheritance.
3. **Headers:** Every major entry file must have a `// This file handles...` header.
4. **Testing:** Use Playwright for E2E and Vitest for unit tests.

---

**AI Instruction:** Adhere to these standards when generating or refactoring code.
