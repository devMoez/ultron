# 🌌 Ultron: The Ultimate AI Coding Companion

> "Think Jarvis, but for your terminal."

Ultron is a high-performance, personalized AI assistant built on the foundations of [OpenCode](https://github.com/anomalyco/opencode). It’s not just a fork; it’s an evolution—tailored for deep Windows integration, advanced automation, and a memory system that grows with you.

---

## 🚀 Key Features

- **💻 Desktop Mastery** – Seamless control over your Windows environment. Move windows, take screenshots, and manage files through natural language.
- **🌐 Autonomous Browsing** – Powered by Playwright and MCP, Ultron can navigate the web, extract data, and perform complex research tasks.
- **🧠 Persistent Intelligence** – A multi-layered memory system that remembers your coding style, project preferences, and past decisions across sessions.
- **🎭 Persona Engine** – Switch between specialized AI personalities like `Beast` for speed, `Codex` for architectural deep-dives, or `Trinity` for full-stack logic.
- **⚡ Swarm Intelligence** – A multi-agent system that parallelizes tasks, from planning and design to debugging and verification.

## 🛠️ Installation

Ultron requires [Bun](https://bun.sh/) for maximum performance.

```bash
# Clone the intelligence
git clone https://github.com/devMoez/ultron.git
cd ultron

# Install dependencies and build
bun install
bun build

# Link the global command
bun link
```

## ⌨️ Usage

Launch Ultron directly from your terminal:

```bash
ultron          # Enter the interactive command center
ultron --chat   # Quick chat mode for rapid queries
ultron tui      # Launch the immersive Terminal User Interface
```

## 📂 Project Structure

| Component | Path | Description |
|-----------|------|-------------|
| **Core** | `packages/opencode` | The engine driving the intelligence. |
| **Swarm** | `swarm/` | Python-based multi-agent orchestration. |
| **Identity** | `.opencode/agent/` | Where Ultron's personality and instructions live. |
| **Memory** | `memory/` | Persistent storage for learned contexts. |

## 🧪 The Swarm

Ultron isn't a single model; it's a hive mind. The Swarm system allows multiple specialized agents to work in parallel on your codebase.

- **Planner**: Deconstructs complex requests.
- **Builder**: Executes high-fidelity code generation.
- **Debugger**: Identifies and fixes regressions instantly.

Check out [SWARM_INTEGRATION.md](./SWARM_INTEGRATION.md) for a deep dive.

---

## 🛡️ Disclaimer

Ultron is a personal labor of love. While built on OpenCode, it is an independent project optimized for my specific workflow. Use it at your own risk, but enjoy the power it brings to your terminal.

Developed with ❤️ by [@devMoez](https://github.com/devMoez)
