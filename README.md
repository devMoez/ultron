# Ultron

Personal AI coding assistant built on OpenCode. Think Jarvis meets your terminal.

## What is this?

This is mycustom fork of OpenCode - renamed "Ultron" and packed with personal tools for Windows automation, browser control, and memory that actually remembers things between sessions.

Credit goes to [anomalyco/opencode](https://github.com/anomalyco/opencode) for the base.

## Features

- **Desktop Control** - Mouse, keyboard, screenshots, window management straight from chat
- **Browser Automation** - Playwright-powered browser control via MCP
- **Persistent Memory** - Remembers your preferences, past decisions, what worked and what didn't
- **Custom Prompts** - Different AI personalities (beast, codex, trinity, etc.)
- ** Caveman Mode** - When you want answers, not essays

## Installation

```bash
# Clone or download
git clone https://github.com/devMoez/ultron.git
cd ultron

# Build (requires Bun)
bun install
bun build

# Run
bun start
# or
node packages/opencode/bin/ultron.cjs
```

## Usage

```
ultron              # Start chat
ultron --chat       # Chat mode
ultron tui          # Terminal UI
```

## Key Customizations

| Feature | File |
|---------|------|
| Memory | `ultron_memory.json` |
| Custom prompts | `packages/opencode/src/session/prompt/*.txt` |
| Skills | `.opencode/skills/*.skill` |
| MCP config | `.opencode/opencode.jsonc` |

## Disclaimer

This is a personal project. Not affiliated with OpenCode team. Built for my own workflow - might not make sense to anyone else.

---

Built by [@devMoez](https://github.com/devMoez)