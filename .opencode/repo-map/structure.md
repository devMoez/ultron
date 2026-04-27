# 📂 Ultron Repository Structure

This file provides a comprehensive index of all major directories and their responsibilities to save AI exploration tokens.

## 🏛️ Core Pillars

| Path | Component | Responsibility |
|------|-----------|----------------|
| `packages/opencode/` | **The Engine** | Core TypeScript logic, CLI handling, and tool execution. |
| `swarm/` | **The Swarm** | Python-based multi-agent orchestration and task parallelization. |
| `ultron-system/` | **The System** | Dashboard, local UI, and background automation services. |

## 📦 Packages Index (`packages/`)

| Folder | Purpose |
|--------|---------|
| `app/` | Desktop/TUI application frontend (Vite/React). |
| `console/` | Console-based UI and CLI interaction layer. |
| `sdk/` | Client SDKs (JS/TS) and OpenAPI specifications. |
| `shared/` | Shared types, utilities, and constants used across packages. |
| `identity/` | Authentication and user session management. |
| `ui/` | Shared React component library. |
| `web/` | Web-based interface for remote access. |

## ⚙️ Configuration & Metadata

| Path | Purpose |
|------|---------|
| `.opencode/` | Global agent personalities, skills, and configuration. |
| `infra/` | Cloud infrastructure (SST/AWS) definitions. |
| `memory/` | Persistent state and session history. |
| `script/` | Build, release, and maintenance scripts. |

---

**AI Instruction:** Use this map to jump directly to the relevant logic instead of performing recursive directory listings.
