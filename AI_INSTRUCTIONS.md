# 🤖 AI Redirection Instructions

Copy and paste the snippet below as your FIRST message to any new AI session (Claude, Gemini, Cursor, etc.) to optimize token usage.

---

### 📋 Copy/Paste Prompt:

"I am working on the **Ultron/OpenCode** repository. To save token context and avoid redundant searching, please read the **`GEMINI.md`** file at the root immediately. It contains the project map and links to detailed documentation in **`.opencode/repo-map/`**. Do not perform directory listings or broad searches until you have read these files."

---

### 📂 Why this exists:
This repository is a large monorepo with multiple packages (`swarm`, `opencode`, `ultron-system`). Blindly searching these folders can cost **20,000+ tokens** in a single turn. By pointing the AI to the map first, you reduce this to **~2,000 tokens**, saving you money and keeping the AI's "memory" sharp for actual coding.
