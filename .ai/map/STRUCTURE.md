# 📂 Repository Structure

## 🏛️ Categorized Folders

| Path | Category | Responsibility |
|------|----------|----------------|
| `.github\workflows` | **Testing** | Core logic for testing |
| `.opencode` | **UI Components** | Core logic for ui components |
| `.opencode\agent` | **UI Components** | Core logic for ui components |
| `.opencode\plugins` | **UI Components** | Core logic for ui components |
| `.opencode\skills` | **AI / Agents** | Core logic for ai / agents |
| `.opencode\skills\agent-builder` | **UI Components** | Core logic for ui components |
| `packages\app` | **AI / Agents** | Core logic for ai / agents |
| `packages\app\e2e` | **Testing** | Core logic for testing |
| `packages\app\src` | **Testing** | Core logic for testing |
| `packages\app\src\addons` | **Testing** | Core logic for testing |
| `packages\app\src\components` | **UI Components** | Core logic for ui components |
| `packages\app\src\components\prompt-input` | **UI Components** | Core logic for ui components |
| `packages\app\src\components\server` | **UI Components** | Core logic for ui components |
| `packages\app\src\components\session` | **UI Components** | Core logic for ui components |
| `packages\app\src\context` | **Testing** | Core logic for testing |
| `packages\app\src\context\file` | **Testing** | Core logic for testing |
| `packages\app\src\context\global-sync` | **Testing** | Core logic for testing |
| `packages\app\src\i18n` | **Testing** | Core logic for testing |
| `packages\app\src\pages\layout` | **Utilities** | Core logic for utilities |
| `packages\app\src\pages\session` | **Testing** | Core logic for testing |
| `packages\app\src\pages\session\composer` | **Testing** | Core logic for testing |
| `packages\app\src\utils` | **Utilities** | Core logic for utilities |
| `packages\console\app\src\routes` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\api` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\auth` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\bench` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\black` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\black\subscribe` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\brand` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\changelog` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\debug` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\docs` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\download` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\download\[channel]` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\enterprise` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\go` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\legal\privacy-policy` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\legal\terms-of-service` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\s` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\stripe` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\t` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\billing` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\go` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\keys` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\members` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\settings` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\workspace\[id]\usage` | **API / Routing** | Core logic for api / routing |
| `packages\console\app\src\routes\zen` | **API / Routing** | Core logic for api / routing |

## 🌲 Full Tree (Graphified)

```text
├── .clinerules
├── .cursorrules
├── .editorconfig
├── .env
├── .github
│   ├── actions
│   │   ├── setup-bun
│   │   │   └── action.yml
│   │   └── setup-git-committer
│   │       └── action.yml
│   ├── CODEOWNERS
│   ├── ISSUE_TEMPLATE
│   │   ├── bug-report.yml
│   │   ├── config.yml
│   │   ├── feature-request.yml
│   │   └── question.yml
│   ├── publish-python-sdk.yml
│   ├── pull_request_template.md
│   ├── TEAM_MEMBERS
│   ├── VOUCHED.td
│   └── workflows
│       ├── beta.yml
│       ├── close-issues.yml
│       ├── close-stale-prs.yml
│       ├── compliance-close.yml
│       ├── containers.yml
│       ├── daily-issues-recap.yml
│       ├── daily-pr-recap.yml
│       ├── deploy.yml
│       ├── docs-locale-sync.yml
│       ├── docs-update.yml
│       ├── duplicate-issues.yml
│       ├── generate.yml
│       ├── nix-eval.yml
│       ├── nix-hashes.yml
│       ├── notify-discord.yml
│       ├── opencode.yml
│       ├── pr-management.yml
│       ├── pr-standards.yml
│       ├── publish-github-action.yml
│       ├── publish-vscode.yml
│       ├── publish.yml
│       ├── release-github-action.yml
│       ├── review.yml
│       ├── stats.yml
│       ├── storybook.yml
│       ├── sync-zed-extension.yml
│       ├── test.yml
│       ├── triage.yml
│       ├── typecheck.yml
│       ├── vouch-check-issue.yml
│       ├── vouch-check-pr.yml
│       └── vouch-manage-by-issue.yml
├── .gitignore
├── .husky
│   ├── pre-push
│   └── _
│       ├── .gitignore
│       ├── applypatch-msg
│       ├── commit-msg
│       ├── h
│       ├── husky.sh
│       ├── post-applypatch
│       ├── post-checkout
│       ├── post-commit
│       ├── post-merge
│       ├── post-rewrite
│       ├── pre-applypatch
│       ├── pre-auto-gc
│       ├── pre-commit
│       ├── pre-merge-commit
│       ├── pre-push
│       ├── pre-rebase
│       └── prepare-commit-msg
├── .opencode
│   ├── .gitignore
│   ├── agent
│   │   ├── builder.md
│   │   ├── coder.md
│   │   ├── debugger.md
│   │   ├── designer.md
│   │   ├── duplicate-pr.md
│   │   ├── fast.md
│   │   ├── orchestrator.md
│   │   ├── planner.md
│   │   ├── researcher.md
│   │   ├── translator.md
│   │   ├── triage.md
│   │   ├── ultron.md
│   │   └── verifier.md
│   ├── command
│   │   ├── ai-deps.md
│   │   ├── changelog.md
│   │   ├── commit.md
│   │   ├── issues.md
│   │   ├── learn.md
│   │   ├── rmslop.md
│   │   └── spellcheck.md
│   ├── env.d.ts
│   ├── glossary
│   │   ├── ar.md
│   │   ├── br.md
│   │   ├── bs.md
│   │   ├── da.md
│   │   ├── de.md
│   │   ├── es.md
│   │   ├── fr.md
│   │   ├── ja.md
│   │   ├── ko.md
│   │   ├── no.md
│   │   ├── pl.md
│   │   ├── README.md
│   │   ├── ru.md
│   │   ├── th.md
│   │   ├── tr.md
│   │   ├── zh-cn.md
│   │   └── zh-tw.md
│   ├── mcp
│   │   ├── desktop.py
│   │   └── tasksync.py
│   ├── opencode.jsonc
│   ├── package-lock.json
│   ├── package.json
│   ├── plugins
│   │   ├── smoke-theme.json
│   │   └── tui-smoke.tsx
│   ├── repo-map
│   │   ├── flows.md
│   │   ├── structure.md
│   │   └── tech-stack.md
│   ├── skills
│   │   ├── agent-builder
│   │   │   ├── agent-builder.md
│   │   │   └── SKILL.md
│   │   ├── agent-coder
│   │   │   ├── agent-coder.md
│   │   │   └── SKILL.md
│   │   ├── agent-debugger
│   │   │   ├── agent-debugger.md
│   │   │   └── SKILL.md
│   │   ├── agent-designer
│   │   │   ├── agent-designer.md
│   │   │   └── SKILL.md
│   │   ├── agent-planner
│   │   │   ├── agent-planner.md
│   │   │   └── SKILL.md
│   │   ├── agent-researcher
│   │   │   ├── agent-researcher.md
│   │   │   └── SKILL.md
│   │   ├── agent-verifier
│   │   │   ├── agent-verifier.md
│   │   │   └── SKILL.md
│   │   ├── ai-agent-orchestrator.skill
│   │   ├── caveman
│   │   │   ├── caveman.md
│   │   │   └── SKILL.md
│   │   ├── caveman-commit
│   │   │   ├── caveman-commit.md
│   │   │   └── SKILL.md
│   │   ├── caveman-help
│   │   │   ├── caveman-help.md
│   │   │   └── SKILL.md
│   │   ├── caveman-review
│   │   │   ├── caveman-review.md
│   │   │   └── SKILL.md
│   │   ├── compress
│   │   │   ├── caveman-compress.md
│   │   │   ├── scripts
│   │   │   │   ├── benchmark.py
│   │   │   │   ├── cli.py
│   │   │   │   ├── compress.py
│   │   │   │   ├── detect.py
│   │   │   │   ├── validate.py
│   │   │   │   ├── __init__.py
│   │   │   │   └── __main__.py
│   │   │   └── SKILL.md
│   │   ├── effect
│   │   │   └── SKILL.md
│   │   ├── memory-update.skill
│   │   ├── ultimate-memory.skill
│   │   └── ultron-default
│   │       ├── SKILL.md
│   │       └── ultron-default.md
│   ├── themes
│   │   ├── .gitignore
│   │   └── mytheme.json
│   ├── tool
│   │   ├── github-pr-search.ts
│   │   └── github-triage.ts
│   ├── tui.json
│   └── ULTRON_MEMORY.md
├── .oxlintrc.json
├── .prettierignore
├── AGENTS.md
├── AI_INSTRUCTIONS.md
├── bun.lock
├── bunfig.toml
├── CONTRIBUTING.md
├── flake.lock
├── flake.nix
├── GEMINI.md
├── github
│   ├── .gitignore
│   ├── action.yml
│   ├── bun.lock
│   ├── index.ts
│   ├── package.json
│   ├── README.md
│   ├── script
│   │   ├── publish
│   │   └── release
│   ├── sst-env.d.ts
│   └── tsconfig.json
├── infra
│   ├── app.ts
│   ├── console.ts
│   ├── enterprise.ts
│   ├── secret.ts
│   └── stage.ts
├── install
├── LICENSE
├── memory
│   ├── hands_mode.json
│   ├── projects.json
│   ├── sessions.json
│   ├── ultron_memory.json
│   └── user_profiles.json
├── nix
│   ├── desktop.nix
│   ├── hashes.json
│   ├── node_modules.nix
│   ├── opencode.nix
│   └── scripts
│       ├── canonicalize-node-modules.ts
│       └── normalize-bun-binaries.ts
├── opencode.jsonc
├── package.json
├── packages
│   ├── app
│   │   ├── .gitignore
│   │   ├── AGENTS.md
│   │   ├── bunfig.toml
│   │   ├── create-effect-simplification-spec.md
│   │   ├── e2e
│   │   │   ├── todo.spec.ts
│   │   │   └── tsconfig.json
│   │   ├── happydom.ts
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── playwright.config.ts
│   │   ├── public
│   │   │   ├── apple-touch-icon-v3.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── assets
│   │   │   │   └── JetBrainsMonoNerdFontMono-Regular.woff2
│   │   │   ├── favicon-96x96-v3.png
│   │   │   ├── favicon-96x96.png
│   │   │   ├── favicon-v3.ico
│   │   │   ├── favicon-v3.svg
│   │   │   ├── favicon.ico
│   │   │   ├── favicon.svg
│   │   │   ├── oc-theme-preload.js
│   │   │   ├── site.webmanifest
│   │   │   ├── social-share-zen.png
│   │   │   ├── social-share.png
│   │   │   ├── web-app-manifest-192x192.png
│   │   │   ├── web-app-manifest-512x512.png
│   │   │   └── _headers
│   │   ├── README.md
│   │   ├── src
│   │   │   ├── addons
│   │   │   │   ├── serialize.test.ts
│   │   │   │   └── serialize.ts
│   │   │   ├── app.tsx
│   │   │   ├── components
│   │   │   │   ├── debug-bar.tsx
│   │   │   │   ├── dialog-connect-provider.tsx
│   │   │   │   ├── dialog-custom-provider-form.ts
│   │   │   │   ├── dialog-custom-provider.test.ts
│   │   │   │   ├── dialog-custom-provider.tsx
│   │   │   │   ├── dialog-edit-project.tsx
│   │   │   │   ├── dialog-fork.tsx
│   │   │   │   ├── dialog-manage-models.tsx
│   │   │   │   ├── dialog-release-notes.tsx
│   │   │   │   ├── dialog-select-directory.tsx
│   │   │   │   ├── dialog-select-file.tsx
│   │   │   │   ├── dialog-select-mcp.tsx
│   │   │   │   ├── dialog-select-model-unpaid.tsx
│   │   │   │   ├── dialog-select-model.tsx
│   │   │   │   ├── dialog-select-provider.tsx
│   │   │   │   ├── dialog-select-server.tsx
│   │   │   │   ├── dialog-settings.tsx
│   │   │   │   ├── file-tree.test.ts
│   │   │   │   ├── file-tree.tsx
│   │   │   │   ├── link.tsx
│   │   │   │   ├── model-tooltip.tsx
│   │   │   │   ├── prompt-input
│   │   │   │   │   ├── attachments.test.ts
│   │   │   │   │   ├── attachments.ts
│   │   │   │   │   ├── build-request-parts.test.ts
│   │   │   │   │   ├── build-request-parts.ts
│   │   │   │   │   ├── context-items.tsx
│   │   │   │   │   ├── drag-overlay.tsx
│   │   │   │   │   ├── editor-dom.test.ts
│   │   │   │   │   ├── editor-dom.ts
│   │   │   │   │   ├── files.ts
│   │   │   │   │   ├── history.test.ts
│   │   │   │   │   ├── history.ts
│   │   │   │   │   ├── image-attachments.tsx
│   │   │   │   │   ├── paste.ts
│   │   │   │   │   ├── placeholder.test.ts
│   │   │   │   │   ├── placeholder.ts
│   │   │   │   │   ├── slash-popover.tsx
│   │   │   │   │   ├── submit.test.ts
│   │   │   │   │   └── submit.ts
│   │   │   │   ├── prompt-input.tsx
│   │   │   │   ├── server
│   │   │   │   │   └── server-row.tsx
│   │   │   │   ├── session
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── session-context-breakdown.test.ts
│   │   │   │   │   ├── session-context-breakdown.ts
│   │   │   │   │   ├── session-context-format.ts
│   │   │   │   │   ├── session-context-metrics.test.ts
│   │   │   │   │   ├── session-context-metrics.ts
│   │   │   │   │   ├── session-context-tab.tsx
│   │   │   │   │   ├── session-header.tsx
│   │   │   │   │   ├── session-new-view.tsx
│   │   │   │   │   ├── session-sortable-tab.tsx
│   │   │   │   │   └── session-sortable-terminal-tab.tsx
│   │   │   │   ├── session-context-usage.tsx
│   │   │   │   ├── settings-general.tsx
│   │   │   │   ├── settings-keybinds.tsx
│   │   │   │   ├── settings-list.tsx
│   │   │   │   ├── settings-models.tsx
│   │   │   │   ├── settings-providers.tsx
│   │   │   │   ├── status-popover-body.tsx
│   │   │   │   ├── status-popover.tsx
│   │   │   │   ├── swarm-panel.tsx
│   │   │   │   ├── terminal.tsx
│   │   │   │   ├── titlebar-history.test.ts
│   │   │   │   ├── titlebar-history.ts
│   │   │   │   └── titlebar.tsx
│   │   │   ├── constants
│   │   │   │   └── file-picker.ts
│   │   │   ├── context
│   │   │   │   ├── command-keybind.test.ts
│   │   │   │   ├── command.test.ts
│   │   │   │   ├── command.tsx
│   │   │   │   ├── comments.test.ts
│   │   │   │   ├── comments.tsx
│   │   │   │   ├── file
│   │   │   │   │   ├── content-cache.ts
│   │   │   │   │   ├── path.test.ts
│   │   │   │   │   ├── path.ts
│   │   │   │   │   ├── tree-store.ts
│   │   │   │   │   ├── types.ts
│   │   │   │   │   ├── view-cache.ts
│   │   │   │   │   ├── watcher.test.ts
│   │   │   │   │   └── watcher.ts
│   │   │   │   ├── file-content-eviction-accounting.test.ts
│   │   │   │   ├── file.tsx
│   │   │   │   ├── global-sdk.tsx
│   │   │   │   ├── global-sync
│   │   │   │   │   ├── bootstrap.ts
│   │   │   │   │   ├── child-store.test.ts
│   │   │   │   │   ├── child-store.ts
│   │   │   │   │   ├── event-reducer.test.ts
│   │   │   │   │   ├── event-reducer.ts
│   │   │   │   │   ├── eviction.ts
│   │   │   │   │   ├── queue.ts
│   │   │   │   │   ├── session-cache.test.ts
│   │   │   │   │   ├── session-cache.ts
│   │   │   │   │   ├── session-load.ts
│   │   │   │   │   ├── session-prefetch.test.ts
│   │   │   │   │   ├── session-prefetch.ts
│   │   │   │   │   ├── session-trim.test.ts
│   │   │   │   │   ├── session-trim.ts
│   │   │   │   │   ├── types.ts
│   │   │   │   │   ├── utils.test.ts
│   │   │   │   │   └── utils.ts
│   │   │   │   ├── global-sync.test.ts
│   │   │   │   ├── global-sync.tsx
│   │   │   │   ├── highlights.tsx
│   │   │   │   ├── language.tsx
│   │   │   │   ├── layout-scroll.test.ts
│   │   │   │   ├── layout-scroll.ts
│   │   │   │   ├── layout.test.ts
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── local.tsx
│   │   │   │   ├── model-variant.test.ts
│   │   │   │   ├── model-variant.ts
│   │   │   │   ├── models.tsx
│   │   │   │   ├── notification.tsx
│   │   │   │   ├── permission-auto-respond.test.ts
│   │   │   │   ├── permission-auto-respond.ts
│   │   │   │   ├── permission.tsx
│   │   │   │   ├── pinned-store.tsx
│   │   │   │   ├── platform.tsx
│   │   │   │   ├── prompt.tsx
│   │   │   │   ├── sdk.tsx
│   │   │   │   ├── server.tsx
│   │   │   │   ├── session-type.tsx
│   │   │   │   ├── settings.tsx
│   │   │   │   ├── sync-optimistic.test.ts
│   │   │   │   ├── sync.tsx
│   │   │   │   ├── terminal-title.ts
│   │   │   │   ├── terminal.test.ts
│   │   │   │   └── terminal.tsx
│   │   │   ├── custom-elements.d.ts
│   │   │   ├── entry.tsx
│   │   │   ├── env.d.ts
│   │   │   ├── hooks
│   │   │   │   └── use-providers.ts
│   │   │   ├── i18n
│   │   │   │   ├── ar.ts
│   │   │   │   ├── br.ts
│   │   │   │   ├── bs.ts
│   │   │   │   ├── da.ts
│   │   │   │   ├── de.ts
│   │   │   │   ├── en.ts
│   │   │   │   ├── es.ts
│   │   │   │   ├── fr.ts
│   │   │   │   ├── ja.ts
│   │   │   │   ├── ko.ts
│   │   │   │   ├── no.ts
│   │   │   │   ├── parity.test.ts
│   │   │   │   ├── pl.ts
│   │   │   │   ├── ru.ts
│   │   │   │   ├── th.ts
│   │   │   │   ├── tr.ts
│   │   │   │   ├── zh.ts
│   │   │   │   └── zht.ts
│   │   │   ├── index.css
│   │   │   ├── index.ts
│   │   │   ├── pages
│   │   │   │   ├── directory-layout.tsx
│   │   │   │   ├── error.tsx
│   │   │   │   ├── home.tsx
│   │   │   │   ├── layout
│   │   │   │   │   ├── deep-links.ts
│   │   │   │   │   ├── helpers.test.ts
│   │   │   │   │   ├── helpers.ts
│   │   │   │   │   ├── inline-editor.tsx
│   │   │   │   │   ├── sidebar-items.tsx
│   │   │   │   │   ├── sidebar-project.tsx
│   │   │   │   │   ├── sidebar-shell.tsx
│   │   │   │   │   └── sidebar-workspace.tsx
│   │   │   │   ├── layout.tsx
│   │   │   │   ├── session
│   │   │   │   │   ├── composer
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   ├── session-composer-region.tsx
│   │   │   │   │   │   ├── session-composer-state.test.ts
│   │   │   │   │   │   ├── session-composer-state.ts
│   │   │   │   │   │   ├── session-followup-dock.tsx
│   │   │   │   │   │   ├── session-permission-dock.tsx
│   │   │   │   │   │   ├── session-question-dock.tsx
│   │   │   │   │   │   ├── session-request-tree.ts
│   │   │   │   │   │   ├── session-revert-dock.tsx
│   │   │   │   │   │   └── session-todo-dock.tsx
│   │   │   │   │   ├── file-tab-scroll.test.ts
│   │   │   │   │   ├── file-tab-scroll.ts
│   │   │   │   │   ├── file-tabs.tsx
│   │   │   │   │   ├── handoff.ts
│   │   │   │   │   ├── helpers.test.ts
│   │   │   │   │   ├── helpers.ts
│   │   │   │   │   ├── message-gesture.test.ts
│   │   │   │   │   ├── message-gesture.ts
│   │   │   │   │   ├── message-id-from-hash.ts
│   │   │   │   │   ├── message-timeline.tsx
│   │   │   │   │   ├── review-tab.tsx
│   │   │   │   │   ├── session-layout.ts
│   │   │   │   │   ├── session-model-helpers.test.ts
│   │   │   │   │   ├── session-model-helpers.ts
│   │   │   │   │   ├── session-side-panel.tsx
│   │   │   │   │   ├── terminal-label.ts
│   │   │   │   │   ├── terminal-panel.test.ts
│   │   │   │   │   ├── terminal-panel.tsx
│   │   │   │   │   ├── use-session-commands.tsx
│   │   │   │   │   ├── use-session-hash-scroll.test.ts
│   │   │   │   │   └── use-session-hash-scroll.ts
│   │   │   │   └── session.tsx
│   │   │   ├── sst-env.d.ts
│   │   │   ├── theme-preload.test.ts
│   │   │   └── utils
│   │   │       ├── agent.ts
│   │   │       ├── aim.ts
│   │   │       ├── base64.ts
│   │   │       ├── comment-note.ts
│   │   │       ├── cross-mention.ts
│   │   │       ├── diffs.test.ts
│   │   │       ├── diffs.ts
│   │   │       ├── id.ts
│   │   │       ├── notification-click.test.ts
│   │   │       ├── notification-click.ts
│   │   │       ├── persist.test.ts
│   │   │       ├── persist.ts
│   │   │       ├── prompt.test.ts
│   │   │       ├── prompt.ts
│   │   │       ├── runtime-adapters.test.ts
│   │   │       ├── runtime-adapters.ts
│   │   │       ├── same.ts
│   │   │       ├── scoped-cache.test.ts
│   │   │       ├── scoped-cache.ts
│   │   │       ├── server-errors.test.ts
│   │   │       ├── server-errors.ts
│   │   │       ├── server-health.test.ts
│   │   │       ├── server-health.ts
│   │   │       ├── server.ts
│   │   │       ├── session-title.ts
│   │   │       ├── solid-dnd.tsx
│   │   │       ├── sound.ts
│   │   │       ├── tab-draft.ts
│   │   │       ├── terminal-writer.test.ts
│   │   │       ├── terminal-writer.ts
│   │   │       ├── time.ts
│   │   │       ├── uuid.test.ts
│   │   │       ├── uuid.ts
│   │   │       ├── worktree.test.ts
│   │   │       └── worktree.ts
│   │   ├── sst-env.d.ts
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   └── vite.js
│   ├── console
│   │   ├── app
│   │   │   ├── .gitignore
│   │   │   ├── .opencode
│   │   │   │   └── agent
│   │   │   │       └── css.md
│   │   │   ├── package.json
│   │   │   ├── public
│   │   │   │   ├── apple-touch-icon-v3.png
│   │   │   │   ├── apple-touch-icon.png
│   │   │   │   ├── email
│   │   │   │   ├── favicon-96x96-v3.png
│   │   │   │   ├── favicon-96x96.png
│   │   │   │   ├── favicon-v3.ico
│   │   │   │   ├── favicon-v3.svg
│   │   │   │   ├── favicon.ico
│   │   │   │   ├── favicon.svg
│   │   │   │   ├── opencode-brand-assets.zip
│   │   │   │   ├── robots.txt
│   │   │   │   ├── site.webmanifest
│   │   │   │   ├── social-share-black.png
│   │   │   │   ├── social-share-zen.png
│   │   │   │   ├── social-share.png
│   │   │   │   ├── theme.json
│   │   │   │   ├── web-app-manifest-192x192.png
│   │   │   │   └── web-app-manifest-512x512.png
│   │   │   ├── README.md
│   │   │   ├── script
│   │   │   │   └── generate-sitemap.ts
│   │   │   ├── src
│   │   │   │   ├── app.css
│   │   │   │   ├── app.tsx
│   │   │   │   ├── asset
│   │   │   │   │   ├── black
│   │   │   │   │   │   └── hero.png
│   │   │   │   │   ├── brand
│   │   │   │   │   │   ├── opencode-brand-assets.zip
│   │   │   │   │   │   ├── opencode-logo-dark-square.png
│   │   │   │   │   │   ├── opencode-logo-dark-square.svg
│   │   │   │   │   │   ├── opencode-logo-dark.png
│   │   │   │   │   │   ├── opencode-logo-dark.svg
│   │   │   │   │   │   ├── opencode-logo-light-square.png
│   │   │   │   │   │   ├── opencode-logo-light-square.svg
│   │   │   │   │   │   ├── opencode-logo-light.png
│   │   │   │   │   │   ├── opencode-logo-light.svg
│   │   │   │   │   │   ├── opencode-wordmark-dark.png
│   │   │   │   │   │   ├── opencode-wordmark-dark.svg
│   │   │   │   │   │   ├── opencode-wordmark-light.png
│   │   │   │   │   │   ├── opencode-wordmark-light.svg
│   │   │   │   │   │   ├── opencode-wordmark-simple-dark.png
│   │   │   │   │   │   ├── opencode-wordmark-simple-dark.svg
│   │   │   │   │   │   ├── opencode-wordmark-simple-light.png
│   │   │   │   │   │   ├── opencode-wordmark-simple-light.svg
│   │   │   │   │   │   ├── preview-opencode-dark.png
│   │   │   │   │   │   ├── preview-opencode-logo-dark-square.png
│   │   │   │   │   │   ├── preview-opencode-logo-dark.png
│   │   │   │   │   │   ├── preview-opencode-logo-light-square.png
│   │   │   │   │   │   ├── preview-opencode-logo-light.png
│   │   │   │   │   │   ├── preview-opencode-wordmark-dark.png
│   │   │   │   │   │   ├── preview-opencode-wordmark-light.png
│   │   │   │   │   │   ├── preview-opencode-wordmark-simple-dark.png
│   │   │   │   │   │   └── preview-opencode-wordmark-simple-light.png
│   │   │   │   │   ├── go-ornate-dark.svg
│   │   │   │   │   ├── go-ornate-light.svg
│   │   │   │   │   ├── lander
│   │   │   │   │   │   ├── avatar-adam.png
│   │   │   │   │   │   ├── avatar-david.png
│   │   │   │   │   │   ├── avatar-dax.png
│   │   │   │   │   │   ├── avatar-frank.png
│   │   │   │   │   │   ├── avatar-jay.png
│   │   │   │   │   │   ├── brand-assets-dark.svg
│   │   │   │   │   │   ├── brand-assets-light.svg
│   │   │   │   │   │   ├── brand.png
│   │   │   │   │   │   ├── check.svg
│   │   │   │   │   │   ├── copy.svg
│   │   │   │   │   │   ├── desktop-app-icon.png
│   │   │   │   │   │   ├── dock.png
│   │   │   │   │   │   ├── logo-dark.svg
│   │   │   │   │   │   ├── logo-light.svg
│   │   │   │   │   │   ├── opencode-comparison-min.mp4
│   │   │   │   │   │   ├── opencode-comparison-poster.png
│   │   │   │   │   │   ├── opencode-desktop-icon.png
│   │   │   │   │   │   ├── opencode-logo-dark.svg
│   │   │   │   │   │   ├── opencode-logo-light.svg
│   │   │   │   │   │   ├── opencode-min.mp4
│   │   │   │   │   │   ├── opencode-poster.png
│   │   │   │   │   │   ├── opencode-wordmark-dark.svg
│   │   │   │   │   │   ├── opencode-wordmark-light.svg
│   │   │   │   │   │   ├── screenshot-github.png
│   │   │   │   │   │   ├── screenshot-splash.png
│   │   │   │   │   │   ├── screenshot-vscode.png
│   │   │   │   │   │   ├── screenshot.png
│   │   │   │   │   │   ├── wordmark-dark.svg
│   │   │   │   │   │   └── wordmark-light.svg
│   │   │   │   │   ├── logo-ornate-dark.svg
│   │   │   │   │   ├── logo-ornate-light.svg
│   │   │   │   │   ├── logo.svg
│   │   │   │   │   ├── zen-ornate-dark.svg
│   │   │   │   │   └── zen-ornate-light.svg
│   │   │   │   ├── component
│   │   │   │   │   ├── dropdown.css
│   │   │   │   │   ├── dropdown.tsx
│   │   │   │   │   ├── email-signup.tsx
│   │   │   │   │   ├── faq.tsx
│   │   │   │   │   ├── footer.tsx
│   │   │   │   │   ├── header-context-menu.css
│   │   │   │   │   ├── header.tsx
│   │   │   │   │   ├── icon.tsx
│   │   │   │   │   ├── language-picker.css
│   │   │   │   │   ├── language-picker.tsx
│   │   │   │   │   ├── legal.tsx
│   │   │   │   │   ├── locale-links.tsx
│   │   │   │   │   ├── modal.css
│   │   │   │   │   ├── modal.tsx
│   │   │   │   │   ├── spotlight.css
│   │   │   │   │   └── spotlight.tsx
│   │   │   │   ├── config.ts
│   │   │   │   ├── context
│   │   │   │   │   ├── auth.session.ts
│   │   │   │   │   ├── auth.ts
│   │   │   │   │   ├── auth.withActor.ts
│   │   │   │   │   ├── i18n.tsx
│   │   │   │   │   └── language.tsx
│   │   │   │   ├── entry-client.tsx
│   │   │   │   ├── entry-server.tsx
│   │   │   │   ├── global.d.ts
│   │   │   │   ├── i18n
│   │   │   │   │   ├── ar.ts
│   │   │   │   │   ├── br.ts
│   │   │   │   │   ├── da.ts
│   │   │   │   │   ├── de.ts
│   │   │   │   │   ├── en.ts
│   │   │   │   │   ├── es.ts
│   │   │   │   │   ├── fr.ts
│   │   │   │   │   ├── index.ts
│   │   │   │   │   ├── it.ts
│   │   │   │   │   ├── ja.ts
│   │   │   │   │   ├── ko.ts
│   │   │   │   │   ├── no.ts
│   │   │   │   │   ├── pl.ts
│   │   │   │   │   ├── ru.ts
│   │   │   │   │   ├── th.ts
│   │   │   │   │   ├── tr.ts
│   │   │   │   │   ├── zh.ts
│   │   │   │   │   └── zht.ts
│   │   │   │   ├── lib
│   │   │   │   │   ├── changelog.ts
│   │   │   │   │   ├── form-error.ts
│   │   │   │   │   ├── github.ts
│   │   │   │   │   ├── language.ts
│   │   │   │   │   └── salesforce.ts
│   │   │   │   ├── middleware.ts
│   │   │   │   ├── routes
│   │   │   │   │   ├── api
│   │   │   │   │   │   └── enterprise.ts
│   │   │   │   │   ├── auth
│   │   │   │   │   │   ├── authorize.ts
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   ├── logout.ts
│   │   │   │   │   │   ├── status.ts
│   │   │   │   │   │   └── [...callback].ts
│   │   │   │   │   ├── bench
│   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   ├── submission.ts
│   │   │   │   │   │   └── [id].tsx
│   │   │   │   │   ├── black
│   │   │   │   │   │   ├── common.tsx
│   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   ├── subscribe
│   │   │   │   │   │   │   └── [plan].tsx
│   │   │   │   │   │   ├── workspace.css
│   │   │   │   │   │   └── workspace.tsx
│   │   │   │   │   ├── black.css
│   │   │   │   │   ├── black.tsx
│   │   │   │   │   ├── brand
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── changelog
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── changelog.json.ts
│   │   │   │   │   ├── debug
│   │   │   │   │   │   └── index.ts
│   │   │   │   │   ├── desktop-feedback.ts
│   │   │   │   │   ├── discord.ts
│   │   │   │   │   ├── docs
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   └── [...path].ts
│   │   │   │   │   ├── download
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   ├── types.ts
│   │   │   │   │   │   └── [channel]
│   │   │   │   │   │       └── [platform].ts
│   │   │   │   │   ├── enterprise
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── feishu.ts
│   │   │   │   │   ├── go
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   └── index.tsx
│   │   │   │   │   ├── index.css
│   │   │   │   │   ├── index.tsx
│   │   │   │   │   ├── legal
│   │   │   │   │   │   ├── privacy-policy
│   │   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   │   └── index.tsx
│   │   │   │   │   │   └── terms-of-service
│   │   │   │   │   │       ├── index.css
│   │   │   │   │   │       └── index.tsx
│   │   │   │   │   ├── openapi.json.ts
│   │   │   │   │   ├── s
│   │   │   │   │   │   └── [id].ts
│   │   │   │   │   ├── stripe
│   │   │   │   │   │   └── webhook.ts
│   │   │   │   │   ├── t
│   │   │   │   │   │   └── [...path].tsx
│   │   │   │   │   ├── temp.tsx
│   │   │   │   │   ├── user-menu.css
│   │   │   │   │   ├── user-menu.tsx
│   │   │   │   │   ├── workspace
│   │   │   │   │   │   ├── common.tsx
│   │   │   │   │   │   ├── [id]
│   │   │   │   │   │   │   ├── billing
│   │   │   │   │   │   │   │   ├── billing-section.module.css
│   │   │   │   │   │   │   │   ├── billing-section.tsx
│   │   │   │   │   │   │   │   ├── black-section.module.css
│   │   │   │   │   │   │   │   ├── black-section.tsx
│   │   │   │   │   │   │   │   ├── black-waitlist-section.module.css
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── monthly-limit-section.module.css
│   │   │   │   │   │   │   │   ├── monthly-limit-section.tsx
│   │   │   │   │   │   │   │   ├── payment-section.module.css
│   │   │   │   │   │   │   │   ├── payment-section.tsx
│   │   │   │   │   │   │   │   ├── redeem-section.module.css
│   │   │   │   │   │   │   │   ├── redeem-section.tsx
│   │   │   │   │   │   │   │   ├── reload-section.module.css
│   │   │   │   │   │   │   │   └── reload-section.tsx
│   │   │   │   │   │   │   ├── go
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── lite-section.module.css
│   │   │   │   │   │   │   │   └── lite-section.tsx
│   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   ├── keys
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── key-section.module.css
│   │   │   │   │   │   │   │   └── key-section.tsx
│   │   │   │   │   │   │   ├── members
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── member-section.module.css
│   │   │   │   │   │   │   │   ├── member-section.tsx
│   │   │   │   │   │   │   │   ├── role-dropdown.css
│   │   │   │   │   │   │   │   └── role-dropdown.tsx
│   │   │   │   │   │   │   ├── model-section.module.css
│   │   │   │   │   │   │   ├── model-section.tsx
│   │   │   │   │   │   │   ├── new-user-section.module.css
│   │   │   │   │   │   │   ├── new-user-section.tsx
│   │   │   │   │   │   │   ├── provider-section.module.css
│   │   │   │   │   │   │   ├── provider-section.tsx
│   │   │   │   │   │   │   ├── settings
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── settings-section.module.css
│   │   │   │   │   │   │   │   └── settings-section.tsx
│   │   │   │   │   │   │   └── usage
│   │   │   │   │   │   │       ├── graph-section.module.css
│   │   │   │   │   │   │       ├── graph-section.tsx
│   │   │   │   │   │   │       ├── index.tsx
│   │   │   │   │   │   │       ├── usage-section.module.css
│   │   │   │   │   │   │       └── usage-section.tsx
│   │   │   │   │   │   ├── [id].css
│   │   │   │   │   │   └── [id].tsx
│   │   │   │   │   ├── workspace-picker.css
│   │   │   │   │   ├── workspace-picker.tsx
│   │   │   │   │   ├── workspace.css
│   │   │   │   │   ├── workspace.tsx
│   │   │   │   │   ├── zen
│   │   │   │   │   │   ├── go
│   │   │   │   │   │   │   └── v1
│   │   │   │   │   │   │       ├── chat
│   │   │   │   │   │   │       │   └── completions.ts
│   │   │   │   │   │   │       └── messages.ts
│   │   │   │   │   │   ├── index.css
│   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   ├── util
│   │   │   │   │   │   │   ├── dataDumper.ts
│   │   │   │   │   │   │   ├── error.ts
│   │   │   │   │   │   │   ├── handler.ts
│   │   │   │   │   │   │   ├── ipRateLimiter.ts
│   │   │   │   │   │   │   ├── keyRateLimiter.ts
│   │   │   │   │   │   │   ├── logger.ts
│   │   │   │   │   │   │   ├── modelTpmLimiter.ts
│   │   │   │   │   │   │   ├── provider
│   │   │   │   │   │   │   │   ├── anthropic.ts
│   │   │   │   │   │   │   │   ├── google.ts
│   │   │   │   │   │   │   │   ├── openai-compatible.ts
│   │   │   │   │   │   │   │   ├── openai.ts
│   │   │   │   │   │   │   │   └── provider.ts
│   │   │   │   │   │   │   ├── stickyProviderTracker.ts
│   │   │   │   │   │   │   └── trialLimiter.ts
│   │   │   │   │   │   └── v1
│   │   │   │   │   │       ├── chat
│   │   │   │   │   │       │   └── completions.ts
│   │   │   │   │   │       ├── messages.ts
│   │   │   │   │   │       ├── models
│   │   │   │   │   │       │   └── [model].ts
│   │   │   │   │   │       ├── models.ts
│   │   │   │   │   │       └── responses.ts
│   │   │   │   │   ├── [...404].css
│   │   │   │   │   └── [...404].tsx
│   │   │   │   └── style
│   │   │   │       ├── base.css
│   │   │   │       ├── component
│   │   │   │       │   └── button.css
│   │   │   │       ├── index.css
│   │   │   │       ├── reset.css
│   │   │   │       └── token
│   │   │   │           ├── color.css
│   │   │   │           ├── font.css
│   │   │   │           └── space.css
│   │   │   ├── sst-env.d.ts
│   │   │   ├── test
│   │   │   │   └── rateLimiter.test.ts
│   │   │   ├── tsconfig.json
│   │   │   └── vite.config.ts
│   │   ├── core
│   │   │   ├── .gitignore
│   │   │   ├── drizzle.config.ts
│   │   │   ├── migrations
│   │   │   │   ├── 20250902065410_fluffy_raza
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250903035359_serious_whistler
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250911133331_violet_loners
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250911141957_dusty_clint_barton
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250911214917_first_mockingbird
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250911231144_jazzy_skrulls
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250912021148_parallel_gauntlet
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250912161749_familiar_nightshade
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250914213824_eminent_ultimatum
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250914222302_redundant_piledriver
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250914232505_needy_sue_storm
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250915150801_freezing_phil_sheldon
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250915172014_bright_photon
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250915172258_absurd_hobgoblin
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250919135159_demonic_princess_powerful
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250921042124_cloudy_revanche
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250923213126_cold_la_nuit
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250924230623_woozy_thaddeus_ross
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250928163425_nervous_iron_lad
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250928235456_dazzling_cable
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250929181457_supreme_jack_power
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20250929224703_flawless_clea
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251002175032_nice_dreadnoughts
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251002223020_optimal_paibok
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251003202205_early_black_crow
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251003210411_legal_joseph
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251004030300_numerous_prodigy
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251004045106_hot_wong
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251007024345_careful_cerise
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251007043715_panoramic_harrier
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251007230438_ordinary_ultragirl
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251008161718_outgoing_outlaw_kid
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251009021849_white_doctor_doom
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251016175624_cynical_jack_flag
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251016214520_short_bulldozer
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251017015733_narrow_blindfold
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251017024232_slimy_energizer
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251031163113_messy_jackal
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251125223403_famous_magik
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20251228182259_striped_forge
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260105034337_broken_gamora
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260106204919_odd_misty_knight
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260107000117_flat_nightmare
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260107022356_lame_calypso
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260107041522_tiny_captain_midlands
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260107055817_cuddly_diamondback
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260108224422_charming_black_bolt
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260109000245_huge_omega_red
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260109001625_mean_frank_castle
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260109014234_noisy_domino
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260109040130_bumpy_mephistopheles
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260113215232_jazzy_green_goblin
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260113223840_aromatic_agent_zero
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260116213606_gigantic_hardball
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260116224745_numerous_annihilus
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260122190905_moaning_karnak
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260222233442_clever_toxin
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260224043338_nifty_starjammers
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260414235536_lame_wild_child
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260415002256_perpetual_karen_page
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260415002534_far_smasher
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260417071612_tidy_diamondback
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260418195905_shocking_marvel_zombies
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260420184535_aromatic_molten_man
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260420185813_supreme_roxanne_simpson
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260420191234_deep_scarecrow
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   ├── 20260421020842_bizarre_living_tribunal
│   │   │   │   │   ├── migration.sql
│   │   │   │   │   └── snapshot.json
│   │   │   │   └── 20260421023950_nebulous_weapon_omega
│   │   │   │       ├── migration.sql
│   │   │   │       └── snapshot.json
│   │   │   ├── package.json
│   │   │   ├── script
│   │   │   │   ├── black-cancel-waitlist.ts
│   │   │   │   ├── black-gift.ts
│   │   │   │   ├── black-onboard-waitlist.ts
│   │   │   │   ├── black-select-workspaces.ts
│   │   │   │   ├── black-stats.ts
│   │   │   │   ├── black-transfer.ts
│   │   │   │   ├── create-coupon.ts
│   │   │   │   ├── credit-workspace.ts
│   │   │   │   ├── disable-reload.ts
│   │   │   │   ├── freeze-workspace.ts
│   │   │   │   ├── lookup-user.ts
│   │   │   │   ├── promote-limits.ts
│   │   │   │   ├── promote-models.ts
│   │   │   │   ├── pull-models.ts
│   │   │   │   ├── reset-db.ts
│   │   │   │   ├── update-limits.ts
│   │   │   │   └── update-models.ts
│   │   │   ├── src
│   │   │   │   ├── account.ts
│   │   │   │   ├── actor.ts
│   │   │   │   ├── aws.ts
│   │   │   │   ├── billing.ts
│   │   │   │   ├── black.ts
│   │   │   │   ├── context.ts
│   │   │   │   ├── drizzle
│   │   │   │   │   ├── index.ts
│   │   │   │   │   └── types.ts
│   │   │   │   ├── identifier.ts
│   │   │   │   ├── key.ts
│   │   │   │   ├── lite.ts
│   │   │   │   ├── model.ts
│   │   │   │   ├── provider.ts
│   │   │   │   ├── schema
│   │   │   │   │   ├── account.sql.ts
│   │   │   │   │   ├── auth.sql.ts
│   │   │   │   │   ├── benchmark.sql.ts
│   │   │   │   │   ├── billing.sql.ts
│   │   │   │   │   ├── ip.sql.ts
│   │   │   │   │   ├── key.sql.ts
│   │   │   │   │   ├── model.sql.ts
│   │   │   │   │   ├── provider.sql.ts
│   │   │   │   │   ├── user.sql.ts
│   │   │   │   │   └── workspace.sql.ts
│   │   │   │   ├── subscription.ts
│   │   │   │   ├── user.ts
│   │   │   │   ├── util
│   │   │   │   │   ├── date.ts
│   │   │   │   │   ├── env.cloudflare.ts
│   │   │   │   │   ├── fn.ts
│   │   │   │   │   ├── log.ts
│   │   │   │   │   ├── memo.ts
│   │   │   │   │   └── price.ts
│   │   │   │   └── workspace.ts
│   │   │   ├── sst-env.d.ts
│   │   │   ├── test
│   │   │   │   ├── date.test.ts
│   │   │   │   └── subscription.test.ts
│   │   │   └── tsconfig.json
│   │   ├── function
│   │   │   ├── package.json
│   │   │   ├── src
│   │   │   │   ├── auth.ts
│   │   │   │   └── log-processor.ts
│   │   │   ├── sst-env.d.ts
│   │   │   └── tsconfig.json
│   │   ├── mail
│   │   │   ├── emails
│   │   │   │   ├── components.tsx
│   │   │   │   ├── styles.ts
│   │   │   │   └── templates
│   │   │   │       ├── InviteEmail.tsx
│   │   │   │       └── static
│   │   │   │           ├── ibm-plex-mono-latin-400.woff2
│   │   │   │           ├── ibm-plex-mono-latin-500.woff2
│   │   │   │           ├── ibm-plex-mono-latin-600.woff2
│   │   │   │           ├── ibm-plex-mono-latin-700.woff2
│   │   │   │           ├── JetBrainsMono-Medium.woff2
│   │   │   │           ├── JetBrainsMono-Regular.woff2
│   │   │   │           ├── logo.png
│   │   │   │           ├── right-arrow.png
│   │   │   │           ├── rubik-latin.woff2
│   │   │   │           └── zen-logo.png
│   │   │   ├── package.json
│   │   │   └── sst-env.d.ts
│   │   └── resource
│   │       ├── bun.lock
│   │       ├── package.json
│   │       ├── resource.cloudflare.ts
│   │       ├── resource.node.ts
│   │       ├── sst-env.d.ts
│   │       └── tsconfig.json
│   ├── containers
│   │   ├── base
│   │   │   └── Dockerfile
│   │   ├── bun-node
│   │   │   └── Dockerfile
│   │   ├── publish
│   │   │   └── Dockerfile
│   │   ├── README.md
│   │   ├── rust
│   │   │   └── Dockerfile
│   │   ├── script
│   │   │   └── build.ts
│   │   ├── tauri-linux
│   │   │   └── Dockerfile
│   │   └── tsconfig.json
│   ├── desktop
│   │   ├── .gitignore
│   │   ├── AGENTS.md
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── README.md
│   │   ├── scripts
│   │   │   ├── copy-bundles.ts
│   │   │   ├── finalize-latest-json.ts
│   │   │   ├── predev.ts
│   │   │   ├── prepare.ts
│   │   │   └── utils.ts
│   │   ├── src
│   │   │   ├── bindings.ts
│   │   │   ├── cli.ts
│   │   │   ├── entry.tsx
│   │   │   ├── i18n
│   │   │   │   ├── ar.ts
│   │   │   │   ├── br.ts
│   │   │   │   ├── bs.ts
│   │   │   │   ├── da.ts
│   │   │   │   ├── de.ts
│   │   │   │   ├── en.ts
│   │   │   │   ├── es.ts
│   │   │   │   ├── fr.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── ja.ts
│   │   │   │   ├── ko.ts
│   │   │   │   ├── no.ts
│   │   │   │   ├── pl.ts
│   │   │   │   ├── ru.ts
│   │   │   │   ├── zh.ts
│   │   │   │   └── zht.ts
│   │   │   ├── index.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── menu.ts
│   │   │   ├── styles.css
│   │   │   ├── updater.ts
│   │   │   └── webview-zoom.ts
│   │   ├── src-tauri
│   │   │   ├── .gitignore
│   │   │   ├── assets
│   │   │   │   ├── nsis-header.bmp
│   │   │   │   └── nsis-sidebar.bmp
│   │   │   ├── build.rs
│   │   │   ├── capabilities
│   │   │   │   └── default.json
│   │   │   ├── Cargo.lock
│   │   │   ├── Cargo.toml
│   │   │   ├── entitlements.plist
│   │   │   ├── icons
│   │   │   │   ├── beta
│   │   │   │   │   ├── 128x128.png
│   │   │   │   │   ├── 128x128@2x.png
│   │   │   │   │   ├── 32x32.png
│   │   │   │   │   ├── 64x64.png
│   │   │   │   │   ├── android
│   │   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   └── values
│   │   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   │   ├── icon.icns
│   │   │   │   │   ├── icon.ico
│   │   │   │   │   ├── icon.png
│   │   │   │   │   ├── ios
│   │   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   │   ├── Square107x107Logo.png
│   │   │   │   │   ├── Square142x142Logo.png
│   │   │   │   │   ├── Square150x150Logo.png
│   │   │   │   │   ├── Square284x284Logo.png
│   │   │   │   │   ├── Square30x30Logo.png
│   │   │   │   │   ├── Square310x310Logo.png
│   │   │   │   │   ├── Square44x44Logo.png
│   │   │   │   │   ├── Square71x71Logo.png
│   │   │   │   │   ├── Square89x89Logo.png
│   │   │   │   │   └── StoreLogo.png
│   │   │   │   ├── dev
│   │   │   │   │   ├── 128x128.png
│   │   │   │   │   ├── 128x128@2x.png
│   │   │   │   │   ├── 32x32.png
│   │   │   │   │   ├── 64x64.png
│   │   │   │   │   ├── android
│   │   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   └── values
│   │   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   │   ├── icon.icns
│   │   │   │   │   ├── icon.ico
│   │   │   │   │   ├── icon.png
│   │   │   │   │   ├── ios
│   │   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   │   ├── Square107x107Logo.png
│   │   │   │   │   ├── Square142x142Logo.png
│   │   │   │   │   ├── Square150x150Logo.png
│   │   │   │   │   ├── Square284x284Logo.png
│   │   │   │   │   ├── Square30x30Logo.png
│   │   │   │   │   ├── Square310x310Logo.png
│   │   │   │   │   ├── Square44x44Logo.png
│   │   │   │   │   ├── Square71x71Logo.png
│   │   │   │   │   ├── Square89x89Logo.png
│   │   │   │   │   └── StoreLogo.png
│   │   │   │   ├── prod
│   │   │   │   │   ├── 128x128.png
│   │   │   │   │   ├── 128x128@2x.png
│   │   │   │   │   ├── 32x32.png
│   │   │   │   │   ├── 64x64.png
│   │   │   │   │   ├── android
│   │   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   │   └── values
│   │   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   │   ├── icon.icns
│   │   │   │   │   ├── icon.ico
│   │   │   │   │   ├── icon.png
│   │   │   │   │   ├── ios
│   │   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   │   ├── Square107x107Logo.png
│   │   │   │   │   ├── Square142x142Logo.png
│   │   │   │   │   ├── Square150x150Logo.png
│   │   │   │   │   ├── Square284x284Logo.png
│   │   │   │   │   ├── Square30x30Logo.png
│   │   │   │   │   ├── Square310x310Logo.png
│   │   │   │   │   ├── Square44x44Logo.png
│   │   │   │   │   ├── Square71x71Logo.png
│   │   │   │   │   ├── Square89x89Logo.png
│   │   │   │   │   └── StoreLogo.png
│   │   │   │   └── README.md
│   │   │   ├── release
│   │   │   │   └── appstream.metainfo.xml
│   │   │   ├── src
│   │   │   │   ├── cli.rs
│   │   │   │   ├── constants.rs
│   │   │   │   ├── lib.rs
│   │   │   │   ├── linux_display.rs
│   │   │   │   ├── linux_windowing.rs
│   │   │   │   ├── logging.rs
│   │   │   │   ├── main.rs
│   │   │   │   ├── markdown.rs
│   │   │   │   ├── os
│   │   │   │   │   ├── mod.rs
│   │   │   │   │   └── windows.rs
│   │   │   │   ├── server.rs
│   │   │   │   ├── windows.rs
│   │   │   │   └── window_customizer.rs
│   │   │   ├── tauri.beta.conf.json
│   │   │   ├── tauri.conf.json
│   │   │   └── tauri.prod.conf.json
│   │   ├── sst-env.d.ts
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   ├── desktop-electron
│   │   ├── .gitignore
│   │   ├── AGENTS.md
│   │   ├── electron-builder.config.ts
│   │   ├── electron.vite.config.ts
│   │   ├── icons
│   │   │   ├── beta
│   │   │   │   ├── 128x128.png
│   │   │   │   ├── 128x128@2x.png
│   │   │   │   ├── 32x32.png
│   │   │   │   ├── 64x64.png
│   │   │   │   ├── android
│   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   └── values
│   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   ├── dock.png
│   │   │   │   ├── icon.icns
│   │   │   │   ├── icon.ico
│   │   │   │   ├── icon.png
│   │   │   │   ├── ios
│   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   ├── Square107x107Logo.png
│   │   │   │   ├── Square142x142Logo.png
│   │   │   │   ├── Square150x150Logo.png
│   │   │   │   ├── Square284x284Logo.png
│   │   │   │   ├── Square30x30Logo.png
│   │   │   │   ├── Square310x310Logo.png
│   │   │   │   ├── Square44x44Logo.png
│   │   │   │   ├── Square71x71Logo.png
│   │   │   │   ├── Square89x89Logo.png
│   │   │   │   └── StoreLogo.png
│   │   │   ├── dev
│   │   │   │   ├── 128x128.png
│   │   │   │   ├── 128x128@2x.png
│   │   │   │   ├── 32x32.png
│   │   │   │   ├── 64x64.png
│   │   │   │   ├── android
│   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   └── values
│   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   ├── dock.png
│   │   │   │   ├── icon.icns
│   │   │   │   ├── icon.ico
│   │   │   │   ├── icon.png
│   │   │   │   ├── ios
│   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   ├── Square107x107Logo.png
│   │   │   │   ├── Square142x142Logo.png
│   │   │   │   ├── Square150x150Logo.png
│   │   │   │   ├── Square284x284Logo.png
│   │   │   │   ├── Square30x30Logo.png
│   │   │   │   ├── Square310x310Logo.png
│   │   │   │   ├── Square44x44Logo.png
│   │   │   │   ├── Square71x71Logo.png
│   │   │   │   ├── Square89x89Logo.png
│   │   │   │   └── StoreLogo.png
│   │   │   ├── prod
│   │   │   │   ├── 128x128.png
│   │   │   │   ├── 128x128@2x.png
│   │   │   │   ├── 32x32.png
│   │   │   │   ├── 64x64.png
│   │   │   │   ├── android
│   │   │   │   │   ├── mipmap-anydpi-v26
│   │   │   │   │   │   └── ic_launcher.xml
│   │   │   │   │   ├── mipmap-hdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-mdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   ├── mipmap-xxxhdpi
│   │   │   │   │   │   ├── ic_launcher.png
│   │   │   │   │   │   ├── ic_launcher_foreground.png
│   │   │   │   │   │   └── ic_launcher_round.png
│   │   │   │   │   └── values
│   │   │   │   │       └── ic_launcher_background.xml
│   │   │   │   ├── dock.png
│   │   │   │   ├── icon.icns
│   │   │   │   ├── icon.ico
│   │   │   │   ├── icon.png
│   │   │   │   ├── ios
│   │   │   │   │   ├── AppIcon-20x20@1x.png
│   │   │   │   │   ├── AppIcon-20x20@2x-1.png
│   │   │   │   │   ├── AppIcon-20x20@2x.png
│   │   │   │   │   ├── AppIcon-20x20@3x.png
│   │   │   │   │   ├── AppIcon-29x29@1x.png
│   │   │   │   │   ├── AppIcon-29x29@2x-1.png
│   │   │   │   │   ├── AppIcon-29x29@2x.png
│   │   │   │   │   ├── AppIcon-29x29@3x.png
│   │   │   │   │   ├── AppIcon-40x40@1x.png
│   │   │   │   │   ├── AppIcon-40x40@2x-1.png
│   │   │   │   │   ├── AppIcon-40x40@2x.png
│   │   │   │   │   ├── AppIcon-40x40@3x.png
│   │   │   │   │   ├── AppIcon-512@2x.png
│   │   │   │   │   ├── AppIcon-60x60@2x.png
│   │   │   │   │   ├── AppIcon-60x60@3x.png
│   │   │   │   │   ├── AppIcon-76x76@1x.png
│   │   │   │   │   ├── AppIcon-76x76@2x.png
│   │   │   │   │   └── AppIcon-83.5x83.5@2x.png
│   │   │   │   ├── Square107x107Logo.png
│   │   │   │   ├── Square142x142Logo.png
│   │   │   │   ├── Square150x150Logo.png
│   │   │   │   ├── Square284x284Logo.png
│   │   │   │   ├── Square30x30Logo.png
│   │   │   │   ├── Square310x310Logo.png
│   │   │   │   ├── Square44x44Logo.png
│   │   │   │   ├── Square71x71Logo.png
│   │   │   │   ├── Square89x89Logo.png
│   │   │   │   └── StoreLogo.png
│   │   │   └── README.md
│   │   ├── package.json
│   │   ├── README.md
│   │   ├── resources
│   │   │   └── entitlements.plist
│   │   ├── scripts
│   │   │   ├── copy-bundles.ts
│   │   │   ├── copy-icons.ts
│   │   │   ├── finalize-latest-yml.ts
│   │   │   ├── prebuild.ts
│   │   │   ├── predev.ts
│   │   │   ├── prepare.ts
│   │   │   └── utils.ts
│   │   ├── src
│   │   │   ├── main
│   │   │   │   ├── apps.ts
│   │   │   │   ├── constants.ts
│   │   │   │   ├── env.d.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── ipc.ts
│   │   │   │   ├── logging.ts
│   │   │   │   ├── markdown.ts
│   │   │   │   ├── menu.ts
│   │   │   │   ├── migrate.ts
│   │   │   │   ├── server.ts
│   │   │   │   ├── shell-env.test.ts
│   │   │   │   ├── shell-env.ts
│   │   │   │   ├── store.ts
│   │   │   │   └── windows.ts
│   │   │   ├── preload
│   │   │   │   ├── index.ts
│   │   │   │   └── types.ts
│   │   │   └── renderer
│   │   │       ├── cli.ts
│   │   │       ├── env.d.ts
│   │   │       ├── html.test.ts
│   │   │       ├── i18n
│   │   │       │   ├── ar.ts
│   │   │       │   ├── br.ts
│   │   │       │   ├── bs.ts
│   │   │       │   ├── da.ts
│   │   │       │   ├── de.ts
│   │   │       │   ├── en.ts
│   │   │       │   ├── es.ts
│   │   │       │   ├── fr.ts
│   │   │       │   ├── index.ts
│   │   │       │   ├── ja.ts
│   │   │       │   ├── ko.ts
│   │   │       │   ├── no.ts
│   │   │       │   ├── pl.ts
│   │   │       │   ├── ru.ts
│   │   │       │   ├── zh.ts
│   │   │       │   └── zht.ts
│   │   │       ├── index.html
│   │   │       ├── index.tsx
│   │   │       ├── loading.html
│   │   │       ├── loading.tsx
│   │   │       ├── styles.css
│   │   │       ├── updater.ts
│   │   │       └── webview-zoom.ts
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── discord
│   │   ├── .env
│   │   ├── package.json
│   │   ├── src
│   │   │   └── index.ts
│   │   └── start.ps1
│   ├── docs
│   │   ├── ai-tools
│   │   │   ├── claude-code.mdx
│   │   │   ├── cursor.mdx
│   │   │   └── windsurf.mdx
│   │   ├── development.mdx
│   │   ├── docs.json
│   │   ├── essentials
│   │   │   ├── code.mdx
│   │   │   ├── images.mdx
│   │   │   ├── markdown.mdx
│   │   │   ├── navigation.mdx
│   │   │   ├── reusable-snippets.mdx
│   │   │   └── settings.mdx
│   │   ├── favicon-v3.svg
│   │   ├── favicon.svg
│   │   ├── images
│   │   │   ├── checks-passed.png
│   │   │   ├── hero-dark.png
│   │   │   └── hero-light.png
│   │   ├── index.mdx
│   │   ├── LICENSE
│   │   ├── logo
│   │   │   ├── dark.svg
│   │   │   └── light.svg
│   │   ├── openapi.json
│   │   ├── quickstart.mdx
│   │   ├── README.md
│   │   └── snippets
│   │       └── snippet-intro.mdx
│   ├── enterprise
│   │   ├── .gitignore
│   │   ├── package.json
│   │   ├── public
│   │   │   ├── apple-touch-icon-v3.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── favicon-96x96-v3.png
│   │   │   ├── favicon-96x96.png
│   │   │   ├── favicon-v3.ico
│   │   │   ├── favicon-v3.svg
│   │   │   ├── favicon.ico
│   │   │   ├── favicon.svg
│   │   │   ├── site.webmanifest
│   │   │   ├── social-share-zen.png
│   │   │   ├── social-share.png
│   │   │   ├── web-app-manifest-192x192.png
│   │   │   └── web-app-manifest-512x512.png
│   │   ├── README.md
│   │   ├── script
│   │   │   └── scrap.ts
│   │   ├── src
│   │   │   ├── app.css
│   │   │   ├── app.tsx
│   │   │   ├── core
│   │   │   │   ├── share.ts
│   │   │   │   └── storage.ts
│   │   │   ├── custom-elements.d.ts
│   │   │   ├── entry-client.tsx
│   │   │   ├── entry-server.tsx
│   │   │   ├── global.d.ts
│   │   │   └── routes
│   │   │       ├── api
│   │   │       │   └── [...path].ts
│   │   │       ├── index.tsx
│   │   │       ├── share
│   │   │       │   └── [shareID].tsx
│   │   │       ├── share.tsx
│   │   │       └── [...404].tsx
│   │   ├── sst-env.d.ts
│   │   ├── test
│   │   │   └── core
│   │   │       ├── share.test.ts
│   │   │       └── storage.test.ts
│   │   ├── test-debug.ts
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   ├── extensions
│   │   └── zed
│   │       ├── extension.toml
│   │       ├── icons
│   │       │   └── opencode.svg
│   │       └── LICENSE
│   ├── function
│   │   ├── package.json
│   │   ├── src
│   │   │   └── api.ts
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── identity
│   │   ├── mark-192x192.png
│   │   ├── mark-512x512-light.png
│   │   ├── mark-512x512.png
│   │   ├── mark-96x96.png
│   │   ├── mark-light.svg
│   │   └── mark.svg
│   ├── opencode
│   │   ├── .gitignore
│   │   ├── AGENTS.md
│   │   ├── bin
│   │   │   ├── opencode
│   │   │   └── ultron.cjs
│   │   ├── bunfig.toml
│   │   ├── BUN_SHELL_MIGRATION_PLAN.md
│   │   ├── Dockerfile
│   │   ├── drizzle.config.ts
│   │   ├── git
│   │   ├── migration
│   │   │   ├── 20260127222353_familiar_lady_ursula
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260211171708_add_project_commands
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260213144116_wakeful_the_professor
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260225215848_workspace
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260227213759_add_session_workspace_id
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260228203230_blue_harpoon
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260303231226_add_workspace_fields
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260309230000_move_org_to_state
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260312043431_session_message_cursor
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260323234822_events
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   ├── 20260410174513_workspace-name
│   │   │   │   ├── migration.sql
│   │   │   │   └── snapshot.json
│   │   │   └── 20260413175956_chief_energizer
│   │   │       ├── migration.sql
│   │   │       └── snapshot.json
│   │   ├── package.json
│   │   ├── parsers-config.ts
│   │   ├── README.md
│   │   ├── screenshot.ps1
│   │   ├── script
│   │   │   ├── build-node.ts
│   │   │   ├── build.ts
│   │   │   ├── check-migrations.ts
│   │   │   ├── fix-node-pty.ts
│   │   │   ├── generate.ts
│   │   │   ├── postinstall.mjs
│   │   │   ├── publish.ts
│   │   │   ├── run-workspace-server
│   │   │   ├── schema.ts
│   │   │   ├── time.ts
│   │   │   ├── trace-imports.ts
│   │   │   └── upgrade-opentui.ts
│   │   ├── specs
│   │   │   ├── effect
│   │   │   │   ├── facades.md
│   │   │   │   ├── http-api.md
│   │   │   │   ├── instance-context.md
│   │   │   │   ├── loose-ends.md
│   │   │   │   ├── migration.md
│   │   │   │   ├── routes.md
│   │   │   │   ├── schema.md
│   │   │   │   ├── server-package.md
│   │   │   │   └── tools.md
│   │   │   ├── tui-plugins.md
│   │   │   └── v2
│   │   │       ├── keymappings.md
│   │   │       └── message-shape.md
│   │   ├── src
│   │   │   ├── account
│   │   │   │   ├── account.sql.ts
│   │   │   │   ├── account.ts
│   │   │   │   ├── repo.ts
│   │   │   │   ├── schema.ts
│   │   │   │   └── url.ts
│   │   │   ├── acp
│   │   │   │   ├── agent.ts
│   │   │   │   ├── README.md
│   │   │   │   ├── session.ts
│   │   │   │   └── types.ts
│   │   │   ├── agent
│   │   │   │   ├── agent.ts
│   │   │   │   ├── generate.txt
│   │   │   │   └── prompt
│   │   │   │       ├── compaction.txt
│   │   │   │       ├── explore.txt
│   │   │   │       ├── summary.txt
│   │   │   │       └── title.txt
│   │   │   ├── audio.d.ts
│   │   │   ├── auth
│   │   │   │   └── index.ts
│   │   │   ├── bus
│   │   │   │   ├── bus-event.ts
│   │   │   │   ├── global.ts
│   │   │   │   └── index.ts
│   │   │   ├── cli
│   │   │   │   ├── bootstrap.ts
│   │   │   │   ├── cmd
│   │   │   │   │   ├── account.ts
│   │   │   │   │   ├── acp.ts
│   │   │   │   │   ├── agent.ts
│   │   │   │   │   ├── cmd.ts
│   │   │   │   │   ├── db.ts
│   │   │   │   │   ├── debug
│   │   │   │   │   │   ├── agent.ts
│   │   │   │   │   │   ├── config.ts
│   │   │   │   │   │   ├── file.ts
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   ├── lsp.ts
│   │   │   │   │   │   ├── ripgrep.ts
│   │   │   │   │   │   ├── scrap.ts
│   │   │   │   │   │   ├── skill.ts
│   │   │   │   │   │   └── snapshot.ts
│   │   │   │   │   ├── export.ts
│   │   │   │   │   ├── generate.ts
│   │   │   │   │   ├── github.ts
│   │   │   │   │   ├── import.ts
│   │   │   │   │   ├── mcp.ts
│   │   │   │   │   ├── models.ts
│   │   │   │   │   ├── plug.ts
│   │   │   │   │   ├── pr.ts
│   │   │   │   │   ├── providers.ts
│   │   │   │   │   ├── run.ts
│   │   │   │   │   ├── serve.ts
│   │   │   │   │   ├── session.ts
│   │   │   │   │   ├── stats.ts
│   │   │   │   │   ├── tui
│   │   │   │   │   │   ├── app.tsx
│   │   │   │   │   │   ├── asset
│   │   │   │   │   │   │   ├── charge.wav
│   │   │   │   │   │   │   ├── pulse-a.wav
│   │   │   │   │   │   │   ├── pulse-b.wav
│   │   │   │   │   │   │   └── pulse-c.wav
│   │   │   │   │   │   ├── attach.ts
│   │   │   │   │   │   ├── component
│   │   │   │   │   │   │   ├── bg-pulse.tsx
│   │   │   │   │   │   │   ├── border.tsx
│   │   │   │   │   │   │   ├── dialog-agent.tsx
│   │   │   │   │   │   │   ├── dialog-command.tsx
│   │   │   │   │   │   │   ├── dialog-console-org.tsx
│   │   │   │   │   │   │   ├── dialog-go-upsell.tsx
│   │   │   │   │   │   │   ├── dialog-mcp.tsx
│   │   │   │   │   │   │   ├── dialog-model.tsx
│   │   │   │   │   │   │   ├── dialog-provider.tsx
│   │   │   │   │   │   │   ├── dialog-session-delete-failed.tsx
│   │   │   │   │   │   │   ├── dialog-session-list.tsx
│   │   │   │   │   │   │   ├── dialog-session-rename.tsx
│   │   │   │   │   │   │   ├── dialog-skill.tsx
│   │   │   │   │   │   │   ├── dialog-stash.tsx
│   │   │   │   │   │   │   ├── dialog-status.tsx
│   │   │   │   │   │   │   ├── dialog-tag.tsx
│   │   │   │   │   │   │   ├── dialog-theme-list.tsx
│   │   │   │   │   │   │   ├── dialog-variant.tsx
│   │   │   │   │   │   │   ├── dialog-workspace-create.tsx
│   │   │   │   │   │   │   ├── dialog-workspace-unavailable.tsx
│   │   │   │   │   │   │   ├── error-component.tsx
│   │   │   │   │   │   │   ├── logo.tsx
│   │   │   │   │   │   │   ├── plugin-route-missing.tsx
│   │   │   │   │   │   │   ├── prompt
│   │   │   │   │   │   │   │   ├── autocomplete.tsx
│   │   │   │   │   │   │   │   ├── cwd.ts
│   │   │   │   │   │   │   │   ├── frecency.tsx
│   │   │   │   │   │   │   │   ├── history.tsx
│   │   │   │   │   │   │   │   ├── index.tsx
│   │   │   │   │   │   │   │   ├── part.ts
│   │   │   │   │   │   │   │   └── stash.tsx
│   │   │   │   │   │   │   ├── spinner.tsx
│   │   │   │   │   │   │   ├── startup-loading.tsx
│   │   │   │   │   │   │   ├── textarea-keybindings.ts
│   │   │   │   │   │   │   └── todo-item.tsx
│   │   │   │   │   │   ├── config
│   │   │   │   │   │   │   ├── cwd.ts
│   │   │   │   │   │   │   ├── tui-migrate.ts
│   │   │   │   │   │   │   ├── tui-schema.ts
│   │   │   │   │   │   │   └── tui.ts
│   │   │   │   │   │   ├── context
│   │   │   │   │   │   │   ├── args.tsx
│   │   │   │   │   │   │   ├── autopilot.ts
│   │   │   │   │   │   │   ├── directory.ts
│   │   │   │   │   │   │   ├── event.ts
│   │   │   │   │   │   │   ├── exit.tsx
│   │   │   │   │   │   │   ├── helper.tsx
│   │   │   │   │   │   │   ├── keybind.tsx
│   │   │   │   │   │   │   ├── kv.tsx
│   │   │   │   │   │   │   ├── local.tsx
│   │   │   │   │   │   │   ├── plugin-keybinds.ts
│   │   │   │   │   │   │   ├── project.tsx
│   │   │   │   │   │   │   ├── prompt.tsx
│   │   │   │   │   │   │   ├── route.tsx
│   │   │   │   │   │   │   ├── sdk.tsx
│   │   │   │   │   │   │   ├── sync.tsx
│   │   │   │   │   │   │   ├── theme
│   │   │   │   │   │   │   │   ├── aura.json
│   │   │   │   │   │   │   │   ├── ayu.json
│   │   │   │   │   │   │   │   ├── carbonfox.json
│   │   │   │   │   │   │   │   ├── catppuccin-frappe.json
│   │   │   │   │   │   │   │   ├── catppuccin-macchiato.json
│   │   │   │   │   │   │   │   ├── catppuccin.json
│   │   │   │   │   │   │   │   ├── cobalt2.json
│   │   │   │   │   │   │   │   ├── cursor.json
│   │   │   │   │   │   │   │   ├── dracula.json
│   │   │   │   │   │   │   │   ├── everforest.json
│   │   │   │   │   │   │   │   ├── flexoki.json
│   │   │   │   │   │   │   │   ├── github.json
│   │   │   │   │   │   │   │   ├── gruvbox.json
│   │   │   │   │   │   │   │   ├── kanagawa.json
│   │   │   │   │   │   │   │   ├── lucent-orng.json
│   │   │   │   │   │   │   │   ├── material.json
│   │   │   │   │   │   │   │   ├── matrix.json
│   │   │   │   │   │   │   │   ├── mercury.json
│   │   │   │   │   │   │   │   ├── monokai.json
│   │   │   │   │   │   │   │   ├── nightowl.json
│   │   │   │   │   │   │   │   ├── nord.json
│   │   │   │   │   │   │   │   ├── one-dark.json
│   │   │   │   │   │   │   │   ├── opencode.json
│   │   │   │   │   │   │   │   ├── orng.json
│   │   │   │   │   │   │   │   ├── osaka-jade.json
│   │   │   │   │   │   │   │   ├── palenight.json
│   │   │   │   │   │   │   │   ├── rosepine.json
│   │   │   │   │   │   │   │   ├── solarized.json
│   │   │   │   │   │   │   │   ├── synthwave84.json
│   │   │   │   │   │   │   │   ├── tokyonight.json
│   │   │   │   │   │   │   │   ├── vercel.json
│   │   │   │   │   │   │   │   ├── vesper.json
│   │   │   │   │   │   │   │   └── zenburn.json
│   │   │   │   │   │   │   ├── theme.tsx
│   │   │   │   │   │   │   └── tui-config.tsx
│   │   │   │   │   │   ├── event.ts
│   │   │   │   │   │   ├── feature-plugins
│   │   │   │   │   │   │   ├── home
│   │   │   │   │   │   │   │   ├── footer.tsx
│   │   │   │   │   │   │   │   ├── tips-view.tsx
│   │   │   │   │   │   │   │   └── tips.tsx
│   │   │   │   │   │   │   ├── sidebar
│   │   │   │   │   │   │   │   ├── context.tsx
│   │   │   │   │   │   │   │   ├── files.tsx
│   │   │   │   │   │   │   │   ├── footer.tsx
│   │   │   │   │   │   │   │   ├── lsp.tsx
│   │   │   │   │   │   │   │   ├── mcp.tsx
│   │   │   │   │   │   │   │   └── todo.tsx
│   │   │   │   │   │   │   └── system
│   │   │   │   │   │   │       └── plugins.tsx
│   │   │   │   │   │   ├── layer.ts
│   │   │   │   │   │   ├── plugin
│   │   │   │   │   │   │   ├── api.tsx
│   │   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   │   ├── internal.ts
│   │   │   │   │   │   │   ├── runtime.ts
│   │   │   │   │   │   │   └── slots.tsx
│   │   │   │   │   │   ├── routes
│   │   │   │   │   │   │   ├── home.tsx
│   │   │   │   │   │   │   └── session
│   │   │   │   │   │   │       ├── dialog-fork-from-timeline.tsx
│   │   │   │   │   │   │       ├── dialog-message.tsx
│   │   │   │   │   │   │       ├── dialog-subagent.tsx
│   │   │   │   │   │   │       ├── dialog-timeline.tsx
│   │   │   │   │   │   │       ├── footer.tsx
│   │   │   │   │   │   │       ├── index.tsx
│   │   │   │   │   │   │       ├── permission.tsx
│   │   │   │   │   │   │       ├── question.tsx
│   │   │   │   │   │   │       ├── sidebar.tsx
│   │   │   │   │   │   │       └── subagent-footer.tsx
│   │   │   │   │   │   ├── thread.ts
│   │   │   │   │   │   ├── ui
│   │   │   │   │   │   │   ├── dialog-alert.tsx
│   │   │   │   │   │   │   ├── dialog-confirm.tsx
│   │   │   │   │   │   │   ├── dialog-export-options.tsx
│   │   │   │   │   │   │   ├── dialog-help.tsx
│   │   │   │   │   │   │   ├── dialog-prompt.tsx
│   │   │   │   │   │   │   ├── dialog-select.tsx
│   │   │   │   │   │   │   ├── dialog.tsx
│   │   │   │   │   │   │   ├── link.tsx
│   │   │   │   │   │   │   ├── spinner.ts
│   │   │   │   │   │   │   └── toast.tsx
│   │   │   │   │   │   ├── util
│   │   │   │   │   │   │   ├── clipboard.ts
│   │   │   │   │   │   │   ├── editor.ts
│   │   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   │   ├── model.ts
│   │   │   │   │   │   │   ├── provider-origin.ts
│   │   │   │   │   │   │   ├── revert-diff.ts
│   │   │   │   │   │   │   ├── scroll.ts
│   │   │   │   │   │   │   ├── selection.ts
│   │   │   │   │   │   │   ├── signal.ts
│   │   │   │   │   │   │   ├── sound.ts
│   │   │   │   │   │   │   ├── terminal.ts
│   │   │   │   │   │   │   └── transcript.ts
│   │   │   │   │   │   ├── validate-session.ts
│   │   │   │   │   │   ├── win32.ts
│   │   │   │   │   │   └── worker.ts
│   │   │   │   │   ├── uninstall.ts
│   │   │   │   │   ├── upgrade.ts
│   │   │   │   │   └── web.ts
│   │   │   │   ├── effect
│   │   │   │   │   └── prompt.ts
│   │   │   │   ├── error.ts
│   │   │   │   ├── heap.ts
│   │   │   │   ├── logo.ts
│   │   │   │   ├── network.ts
│   │   │   │   ├── ui.ts
│   │   │   │   └── upgrade.ts
│   │   │   ├── command
│   │   │   │   ├── index.ts
│   │   │   │   └── template
│   │   │   │       ├── initialize.txt
│   │   │   │       └── review.txt
│   │   │   ├── config
│   │   │   │   ├── agent.ts
│   │   │   │   ├── command.ts
│   │   │   │   ├── config.ts
│   │   │   │   ├── console-state.ts
│   │   │   │   ├── entry-name.ts
│   │   │   │   ├── error.ts
│   │   │   │   ├── formatter.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── keybinds.ts
│   │   │   │   ├── layout.ts
│   │   │   │   ├── lsp.ts
│   │   │   │   ├── managed.ts
│   │   │   │   ├── markdown.ts
│   │   │   │   ├── mcp.ts
│   │   │   │   ├── model-id.ts
│   │   │   │   ├── parse.ts
│   │   │   │   ├── paths.ts
│   │   │   │   ├── permission.ts
│   │   │   │   ├── plugin.ts
│   │   │   │   ├── provider.ts
│   │   │   │   ├── server.ts
│   │   │   │   ├── skills.ts
│   │   │   │   └── variable.ts
│   │   │   ├── control-plane
│   │   │   │   ├── adaptors
│   │   │   │   │   ├── index.ts
│   │   │   │   │   └── worktree.ts
│   │   │   │   ├── dev
│   │   │   │   │   └── debug-workspace-plugin.ts
│   │   │   │   ├── schema.ts
│   │   │   │   ├── sse.ts
│   │   │   │   ├── types.ts
│   │   │   │   ├── util.ts
│   │   │   │   ├── workspace-context.ts
│   │   │   │   ├── workspace.sql.ts
│   │   │   │   └── workspace.ts
│   │   │   ├── effect
│   │   │   │   ├── app-runtime.ts
│   │   │   │   ├── bootstrap-runtime.ts
│   │   │   │   ├── bridge.ts
│   │   │   │   ├── cross-spawn-spawner.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── instance-ref.ts
│   │   │   │   ├── instance-registry.ts
│   │   │   │   ├── instance-state.ts
│   │   │   │   ├── logger.ts
│   │   │   │   ├── memo-map.ts
│   │   │   │   ├── observability.ts
│   │   │   │   ├── run-service.ts
│   │   │   │   ├── runner.ts
│   │   │   │   └── runtime.ts
│   │   │   ├── env
│   │   │   │   └── index.ts
│   │   │   ├── file
│   │   │   │   ├── ignore.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── protected.ts
│   │   │   │   ├── ripgrep.ts
│   │   │   │   └── watcher.ts
│   │   │   ├── flag
│   │   │   │   └── flag.ts
│   │   │   ├── format
│   │   │   │   ├── formatter.ts
│   │   │   │   └── index.ts
│   │   │   ├── git
│   │   │   │   └── index.ts
│   │   │   ├── global
│   │   │   │   └── index.ts
│   │   │   ├── id
│   │   │   │   └── id.ts
│   │   │   ├── ide
│   │   │   │   └── index.ts
│   │   │   ├── index.ts
│   │   │   ├── installation
│   │   │   │   ├── index.ts
│   │   │   │   └── version.ts
│   │   │   ├── lsp
│   │   │   │   ├── client.ts
│   │   │   │   ├── diagnostic.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── language.ts
│   │   │   │   ├── launch.ts
│   │   │   │   ├── lsp.ts
│   │   │   │   └── server.ts
│   │   │   ├── mcp
│   │   │   │   ├── auth.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── oauth-callback.ts
│   │   │   │   └── oauth-provider.ts
│   │   │   ├── node.ts
│   │   │   ├── npm
│   │   │   │   ├── config.ts
│   │   │   │   └── index.ts
│   │   │   ├── npmcli-config.d.ts
│   │   │   ├── patch
│   │   │   │   └── index.ts
│   │   │   ├── permission
│   │   │   │   ├── arity.ts
│   │   │   │   ├── evaluate.ts
│   │   │   │   ├── index.ts
│   │   │   │   └── schema.ts
│   │   │   ├── plugin
│   │   │   │   ├── cloudflare.ts
│   │   │   │   ├── codex.ts
│   │   │   │   ├── github-copilot
│   │   │   │   │   ├── copilot.ts
│   │   │   │   │   └── models.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── install.ts
│   │   │   │   ├── loader.ts
│   │   │   │   ├── meta.ts
│   │   │   │   └── shared.ts
│   │   │   ├── project
│   │   │   │   ├── bootstrap.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── instance.ts
│   │   │   │   ├── project.sql.ts
│   │   │   │   ├── project.ts
│   │   │   │   ├── schema.ts
│   │   │   │   └── vcs.ts
│   │   │   ├── provider
│   │   │   │   ├── auth.ts
│   │   │   │   ├── error.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── models-snapshot.d.ts
│   │   │   │   ├── models-snapshot.js
│   │   │   │   ├── models.ts
│   │   │   │   ├── provider.ts
│   │   │   │   ├── schema.ts
│   │   │   │   ├── sdk
│   │   │   │   │   └── copilot
│   │   │   │   │       ├── chat
│   │   │   │   │       │   ├── convert-to-openai-compatible-chat-messages.ts
│   │   │   │   │       │   ├── get-response-metadata.ts
│   │   │   │   │       │   ├── map-openai-compatible-finish-reason.ts
│   │   │   │   │       │   ├── openai-compatible-api-types.ts
│   │   │   │   │       │   ├── openai-compatible-chat-language-model.ts
│   │   │   │   │       │   ├── openai-compatible-chat-options.ts
│   │   │   │   │       │   ├── openai-compatible-metadata-extractor.ts
│   │   │   │   │       │   └── openai-compatible-prepare-tools.ts
│   │   │   │   │       ├── copilot-provider.ts
│   │   │   │   │       ├── index.ts
│   │   │   │   │       ├── openai-compatible-error.ts
│   │   │   │   │       ├── README.md
│   │   │   │   │       └── responses
│   │   │   │   │           ├── convert-to-openai-responses-input.ts
│   │   │   │   │           ├── map-openai-responses-finish-reason.ts
│   │   │   │   │           ├── openai-config.ts
│   │   │   │   │           ├── openai-error.ts
│   │   │   │   │           ├── openai-responses-api-types.ts
│   │   │   │   │           ├── openai-responses-language-model.ts
│   │   │   │   │           ├── openai-responses-prepare-tools.ts
│   │   │   │   │           ├── openai-responses-settings.ts
│   │   │   │   │           └── tool
│   │   │   │   │               ├── code-interpreter.ts
│   │   │   │   │               ├── file-search.ts
│   │   │   │   │               ├── image-generation.ts
│   │   │   │   │               ├── local-shell.ts
│   │   │   │   │               ├── web-search-preview.ts
│   │   │   │   │               └── web-search.ts
│   │   │   │   └── transform.ts
│   │   │   ├── pty
│   │   │   │   ├── index.ts
│   │   │   │   ├── pty.bun.ts
│   │   │   │   ├── pty.node.ts
│   │   │   │   ├── pty.ts
│   │   │   │   └── schema.ts
│   │   │   ├── question
│   │   │   │   ├── index.ts
│   │   │   │   └── schema.ts
│   │   │   ├── server
│   │   │   │   ├── adapter.bun.ts
│   │   │   │   ├── adapter.node.ts
│   │   │   │   ├── adapter.ts
│   │   │   │   ├── error.ts
│   │   │   │   ├── event.ts
│   │   │   │   ├── fence.ts
│   │   │   │   ├── mdns.ts
│   │   │   │   ├── middleware.ts
│   │   │   │   ├── projectors.ts
│   │   │   │   ├── proxy.ts
│   │   │   │   ├── routes
│   │   │   │   │   ├── control
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   └── workspace.ts
│   │   │   │   │   ├── global.ts
│   │   │   │   │   ├── instance
│   │   │   │   │   │   ├── config.ts
│   │   │   │   │   │   ├── event.ts
│   │   │   │   │   │   ├── experimental.ts
│   │   │   │   │   │   ├── file.ts
│   │   │   │   │   │   ├── httpapi
│   │   │   │   │   │   │   ├── config.ts
│   │   │   │   │   │   │   ├── permission.ts
│   │   │   │   │   │   │   ├── project.ts
│   │   │   │   │   │   │   ├── provider.ts
│   │   │   │   │   │   │   ├── question.ts
│   │   │   │   │   │   │   └── server.ts
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   ├── mcp.ts
│   │   │   │   │   │   ├── middleware.ts
│   │   │   │   │   │   ├── permission.ts
│   │   │   │   │   │   ├── project.ts
│   │   │   │   │   │   ├── provider.ts
│   │   │   │   │   │   ├── pty.ts
│   │   │   │   │   │   ├── question.ts
│   │   │   │   │   │   ├── session.ts
│   │   │   │   │   │   ├── sync.ts
│   │   │   │   │   │   ├── trace.ts
│   │   │   │   │   │   └── tui.ts
│   │   │   │   │   └── ui.ts
│   │   │   │   ├── server.ts
│   │   │   │   ├── static
│   │   │   │   │   └── ultron-sidebar.html
│   │   │   │   └── workspace.ts
│   │   │   ├── session
│   │   │   │   ├── compaction.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── instruction.ts
│   │   │   │   ├── llm.ts
│   │   │   │   ├── message-v2.ts
│   │   │   │   ├── message.ts
│   │   │   │   ├── overflow.ts
│   │   │   │   ├── processor.ts
│   │   │   │   ├── projectors.ts
│   │   │   │   ├── prompt
│   │   │   │   │   ├── anthropic.txt
│   │   │   │   │   ├── beast.txt
│   │   │   │   │   ├── build-switch.txt
│   │   │   │   │   ├── codex.txt
│   │   │   │   │   ├── copilot-gpt-5.txt
│   │   │   │   │   ├── default.txt
│   │   │   │   │   ├── gemini.txt
│   │   │   │   │   ├── gpt.txt
│   │   │   │   │   ├── kimi.txt
│   │   │   │   │   ├── max-steps.txt
│   │   │   │   │   ├── plan-reminder-anthropic.txt
│   │   │   │   │   ├── plan.txt
│   │   │   │   │   └── trinity.txt
│   │   │   │   ├── prompt.ts
│   │   │   │   ├── retry.ts
│   │   │   │   ├── revert.ts
│   │   │   │   ├── run-state.ts
│   │   │   │   ├── schema.ts
│   │   │   │   ├── session.sql.ts
│   │   │   │   ├── session.ts
│   │   │   │   ├── status.ts
│   │   │   │   ├── summary.ts
│   │   │   │   ├── system.ts
│   │   │   │   └── todo.ts
│   │   │   ├── share
│   │   │   │   ├── index.ts
│   │   │   │   ├── session.ts
│   │   │   │   ├── share-next.ts
│   │   │   │   └── share.sql.ts
│   │   │   ├── shell
│   │   │   │   └── shell.ts
│   │   │   ├── skill
│   │   │   │   ├── discovery.ts
│   │   │   │   └── index.ts
│   │   │   ├── snapshot
│   │   │   │   └── index.ts
│   │   │   ├── sql.d.ts
│   │   │   ├── storage
│   │   │   │   ├── db.bun.ts
│   │   │   │   ├── db.node.ts
│   │   │   │   ├── db.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── json-migration.ts
│   │   │   │   ├── schema.sql.ts
│   │   │   │   ├── schema.ts
│   │   │   │   └── storage.ts
│   │   │   ├── sync
│   │   │   │   ├── event.sql.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── README.md
│   │   │   │   └── schema.ts
│   │   │   ├── temporary.ts
│   │   │   ├── tool
│   │   │   │   ├── apply_patch.ts
│   │   │   │   ├── apply_patch.txt
│   │   │   │   ├── bash.ts
│   │   │   │   ├── bash.txt
│   │   │   │   ├── codesearch.ts
│   │   │   │   ├── codesearch.txt
│   │   │   │   ├── edit.ts
│   │   │   │   ├── edit.txt
│   │   │   │   ├── external-directory.ts
│   │   │   │   ├── glob.ts
│   │   │   │   ├── glob.txt
│   │   │   │   ├── grep.ts
│   │   │   │   ├── grep.txt
│   │   │   │   ├── index.ts
│   │   │   │   ├── invalid.ts
│   │   │   │   ├── lsp.ts
│   │   │   │   ├── lsp.txt
│   │   │   │   ├── manage_software.ts
│   │   │   │   ├── mcp-exa.ts
│   │   │   │   ├── open_app.ts
│   │   │   │   ├── plan-enter.txt
│   │   │   │   ├── plan-exit.txt
│   │   │   │   ├── plan.ts
│   │   │   │   ├── question.ts
│   │   │   │   ├── question.txt
│   │   │   │   ├── read.ts
│   │   │   │   ├── read.txt
│   │   │   │   ├── registry.ts
│   │   │   │   ├── schema.ts
│   │   │   │   ├── search_system.ts
│   │   │   │   ├── send_notification.ts
│   │   │   │   ├── skill.ts
│   │   │   │   ├── skill.txt
│   │   │   │   ├── system_info.ts
│   │   │   │   ├── system_power.ts
│   │   │   │   ├── task.ts
│   │   │   │   ├── task.txt
│   │   │   │   ├── todo.ts
│   │   │   │   ├── todowrite.txt
│   │   │   │   ├── tool.ts
│   │   │   │   ├── truncate.ts
│   │   │   │   ├── truncation-dir.ts
│   │   │   │   ├── webfetch.ts
│   │   │   │   ├── webfetch.txt
│   │   │   │   ├── websearch.ts
│   │   │   │   ├── websearch.txt
│   │   │   │   ├── write.ts
│   │   │   │   └── write.txt
│   │   │   ├── util
│   │   │   │   ├── abort.ts
│   │   │   │   ├── archive.ts
│   │   │   │   ├── bom.ts
│   │   │   │   ├── color.ts
│   │   │   │   ├── data-url.ts
│   │   │   │   ├── defer.ts
│   │   │   │   ├── effect-http-client.ts
│   │   │   │   ├── effect-zod.ts
│   │   │   │   ├── error.ts
│   │   │   │   ├── filesystem.ts
│   │   │   │   ├── fn.ts
│   │   │   │   ├── format.ts
│   │   │   │   ├── iife.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── keybind.ts
│   │   │   │   ├── lazy.ts
│   │   │   │   ├── local-context.ts
│   │   │   │   ├── locale.ts
│   │   │   │   ├── lock.ts
│   │   │   │   ├── log.ts
│   │   │   │   ├── media.ts
│   │   │   │   ├── named-schema-error.ts
│   │   │   │   ├── network.ts
│   │   │   │   ├── opencode-process.ts
│   │   │   │   ├── process.ts
│   │   │   │   ├── queue.ts
│   │   │   │   ├── record.ts
│   │   │   │   ├── rpc.ts
│   │   │   │   ├── schema.ts
│   │   │   │   ├── scrap.ts
│   │   │   │   ├── signal.ts
│   │   │   │   ├── timeout.ts
│   │   │   │   ├── token.ts
│   │   │   │   ├── update-schema.ts
│   │   │   │   ├── which.ts
│   │   │   │   └── wildcard.ts
│   │   │   ├── v2
│   │   │   │   ├── session-entry-stepper.ts
│   │   │   │   ├── session-entry.ts
│   │   │   │   ├── session-event.ts
│   │   │   │   └── session.ts
│   │   │   └── worktree
│   │   │       └── index.ts
│   │   ├── sst-env.d.ts
│   │   ├── test
│   │   │   ├── account
│   │   │   │   ├── repo.test.ts
│   │   │   │   └── service.test.ts
│   │   │   ├── acp
│   │   │   │   ├── agent-interface.test.ts
│   │   │   │   └── event-subscription.test.ts
│   │   │   ├── agent
│   │   │   │   └── agent.test.ts
│   │   │   ├── AGENTS.md
│   │   │   ├── auth
│   │   │   │   └── auth.test.ts
│   │   │   ├── bus
│   │   │   │   ├── bus-effect.test.ts
│   │   │   │   ├── bus-integration.test.ts
│   │   │   │   └── bus.test.ts
│   │   │   ├── cli
│   │   │   │   ├── account.test.ts
│   │   │   │   ├── cmd
│   │   │   │   │   └── tui
│   │   │   │   │       └── prompt-part.test.ts
│   │   │   │   ├── error.test.ts
│   │   │   │   ├── github-action.test.ts
│   │   │   │   ├── github-remote.test.ts
│   │   │   │   ├── import.test.ts
│   │   │   │   ├── plugin-auth-picker.test.ts
│   │   │   │   └── tui
│   │   │   │       ├── keybind-plugin.test.ts
│   │   │   │       ├── plugin-add.test.ts
│   │   │   │       ├── plugin-install.test.ts
│   │   │   │       ├── plugin-lifecycle.test.ts
│   │   │   │       ├── plugin-loader-entrypoint.test.ts
│   │   │   │       ├── plugin-loader-pure.test.ts
│   │   │   │       ├── plugin-loader.test.ts
│   │   │   │       ├── plugin-toggle.test.ts
│   │   │   │       ├── revert-diff.test.ts
│   │   │   │       ├── slot-replace.test.tsx
│   │   │   │       ├── theme-store.test.ts
│   │   │   │       ├── thread.test.ts
│   │   │   │       ├── transcript.test.ts
│   │   │   │       └── use-event.test.tsx
│   │   │   ├── config
│   │   │   │   ├── agent-color.test.ts
│   │   │   │   ├── config.test.ts
│   │   │   │   ├── fixtures
│   │   │   │   │   ├── empty-frontmatter.md
│   │   │   │   │   ├── frontmatter.md
│   │   │   │   │   ├── markdown-header.md
│   │   │   │   │   ├── no-frontmatter.md
│   │   │   │   │   └── weird-model-id.md
│   │   │   │   ├── lsp.test.ts
│   │   │   │   ├── markdown.test.ts
│   │   │   │   ├── plugin.test.ts
│   │   │   │   └── tui.test.ts
│   │   │   ├── control-plane
│   │   │   │   ├── adaptors.test.ts
│   │   │   │   └── sse.test.ts
│   │   │   ├── effect
│   │   │   │   ├── app-runtime-logger.test.ts
│   │   │   │   ├── cross-spawn-spawner.test.ts
│   │   │   │   ├── instance-state.test.ts
│   │   │   │   ├── observability.test.ts
│   │   │   │   ├── run-service.test.ts
│   │   │   │   └── runner.test.ts
│   │   │   ├── fake
│   │   │   │   └── provider.ts
│   │   │   ├── file
│   │   │   │   ├── fsmonitor.test.ts
│   │   │   │   ├── ignore.test.ts
│   │   │   │   ├── index.test.ts
│   │   │   │   ├── path-traversal.test.ts
│   │   │   │   ├── ripgrep.test.ts
│   │   │   │   └── watcher.test.ts
│   │   │   ├── filesystem
│   │   │   │   └── filesystem.test.ts
│   │   │   ├── fixture
│   │   │   │   ├── db.ts
│   │   │   │   ├── fixture.test.ts
│   │   │   │   ├── fixture.ts
│   │   │   │   ├── flock-worker.ts
│   │   │   │   ├── lsp
│   │   │   │   │   └── fake-lsp-server.js
│   │   │   │   ├── plug-worker.ts
│   │   │   │   ├── plugin-meta-worker.ts
│   │   │   │   ├── skills
│   │   │   │   │   ├── agents-sdk
│   │   │   │   │   │   ├── references
│   │   │   │   │   │   │   └── callable.md
│   │   │   │   │   │   └── SKILL.md
│   │   │   │   │   ├── cloudflare
│   │   │   │   │   │   └── SKILL.md
│   │   │   │   │   └── index.json
│   │   │   │   ├── tui-plugin.ts
│   │   │   │   └── tui-runtime.ts
│   │   │   ├── format
│   │   │   │   └── format.test.ts
│   │   │   ├── git
│   │   │   │   └── git.test.ts
│   │   │   ├── ide
│   │   │   │   └── ide.test.ts
│   │   │   ├── installation
│   │   │   │   └── installation.test.ts
│   │   │   ├── keybind.test.ts
│   │   │   ├── lib
│   │   │   │   ├── effect.ts
│   │   │   │   ├── filesystem.ts
│   │   │   │   └── llm-server.ts
│   │   │   ├── lsp
│   │   │   │   ├── client.test.ts
│   │   │   │   ├── index.test.ts
│   │   │   │   ├── launch.test.ts
│   │   │   │   └── lifecycle.test.ts
│   │   │   ├── mcp
│   │   │   │   ├── headers.test.ts
│   │   │   │   ├── lifecycle.test.ts
│   │   │   │   ├── oauth-auto-connect.test.ts
│   │   │   │   ├── oauth-browser.test.ts
│   │   │   │   └── oauth-callback.test.ts
│   │   │   ├── memory
│   │   │   │   ├── abort-leak-webfetch.ts
│   │   │   │   └── abort-leak.test.ts
│   │   │   ├── npm.test.ts
│   │   │   ├── patch
│   │   │   │   └── patch.test.ts
│   │   │   ├── permission
│   │   │   │   ├── arity.test.ts
│   │   │   │   └── next.test.ts
│   │   │   ├── permission-task.test.ts
│   │   │   ├── plugin
│   │   │   │   ├── auth-override.test.ts
│   │   │   │   ├── cloudflare.test.ts
│   │   │   │   ├── codex.test.ts
│   │   │   │   ├── github-copilot-models.test.ts
│   │   │   │   ├── install-concurrency.test.ts
│   │   │   │   ├── install.test.ts
│   │   │   │   ├── loader-shared.test.ts
│   │   │   │   ├── meta.test.ts
│   │   │   │   ├── shared.test.ts
│   │   │   │   ├── trigger.test.ts
│   │   │   │   └── workspace-adaptor.test.ts
│   │   │   ├── preload.ts
│   │   │   ├── project
│   │   │   │   ├── migrate-global.test.ts
│   │   │   │   ├── project.test.ts
│   │   │   │   ├── vcs.test.ts
│   │   │   │   ├── worktree-remove.test.ts
│   │   │   │   └── worktree.test.ts
│   │   │   ├── provider
│   │   │   │   ├── amazon-bedrock.test.ts
│   │   │   │   ├── copilot
│   │   │   │   │   ├── convert-to-copilot-messages.test.ts
│   │   │   │   │   └── copilot-chat-model.test.ts
│   │   │   │   ├── gitlab-duo.test.ts
│   │   │   │   ├── provider.test.ts
│   │   │   │   └── transform.test.ts
│   │   │   ├── pty
│   │   │   │   ├── pty-output-isolation.test.ts
│   │   │   │   ├── pty-session.test.ts
│   │   │   │   └── pty-shell.test.ts
│   │   │   ├── question
│   │   │   │   └── question.test.ts
│   │   │   ├── server
│   │   │   │   ├── global-session-list.test.ts
│   │   │   │   ├── project-init-git.test.ts
│   │   │   │   ├── session-actions.test.ts
│   │   │   │   ├── session-list.test.ts
│   │   │   │   ├── session-messages.test.ts
│   │   │   │   ├── session-select.test.ts
│   │   │   │   └── trace-attributes.test.ts
│   │   │   ├── session
│   │   │   │   ├── compaction.test.ts
│   │   │   │   ├── instruction.test.ts
│   │   │   │   ├── llm.test.ts
│   │   │   │   ├── message-v2.test.ts
│   │   │   │   ├── messages-pagination.test.ts
│   │   │   │   ├── processor-effect.test.ts
│   │   │   │   ├── prompt.test.ts
│   │   │   │   ├── retry.test.ts
│   │   │   │   ├── revert-compact.test.ts
│   │   │   │   ├── session-entry-stepper.test.ts
│   │   │   │   ├── session.test.ts
│   │   │   │   ├── snapshot-tool-race.test.ts
│   │   │   │   ├── structured-output-integration.test.ts
│   │   │   │   ├── structured-output.test.ts
│   │   │   │   └── system.test.ts
│   │   │   ├── share
│   │   │   │   └── share-next.test.ts
│   │   │   ├── shell
│   │   │   │   └── shell.test.ts
│   │   │   ├── skill
│   │   │   │   ├── discovery.test.ts
│   │   │   │   └── skill.test.ts
│   │   │   ├── snapshot
│   │   │   │   └── snapshot.test.ts
│   │   │   ├── storage
│   │   │   │   ├── db.test.ts
│   │   │   │   ├── json-migration.test.ts
│   │   │   │   └── storage.test.ts
│   │   │   ├── sync
│   │   │   │   └── index.test.ts
│   │   │   ├── tool
│   │   │   │   ├── apply_patch.test.ts
│   │   │   │   ├── bash.test.ts
│   │   │   │   ├── edit.test.ts
│   │   │   │   ├── external-directory.test.ts
│   │   │   │   ├── fixtures
│   │   │   │   │   ├── large-image.png
│   │   │   │   │   └── models-api.json
│   │   │   │   ├── glob.test.ts
│   │   │   │   ├── grep.test.ts
│   │   │   │   ├── question.test.ts
│   │   │   │   ├── read.test.ts
│   │   │   │   ├── registry.test.ts
│   │   │   │   ├── skill.test.ts
│   │   │   │   ├── task.test.ts
│   │   │   │   ├── tool-define.test.ts
│   │   │   │   ├── truncation.test.ts
│   │   │   │   ├── webfetch.test.ts
│   │   │   │   ├── write.test.ts
│   │   │   │   └── __snapshots__
│   │   │   │       └── tool.test.ts.snap
│   │   │   ├── util
│   │   │   │   ├── data-url.test.ts
│   │   │   │   ├── effect-zod.test.ts
│   │   │   │   ├── error.test.ts
│   │   │   │   ├── filesystem.test.ts
│   │   │   │   ├── format.test.ts
│   │   │   │   ├── glob.test.ts
│   │   │   │   ├── iife.test.ts
│   │   │   │   ├── lazy.test.ts
│   │   │   │   ├── lock.test.ts
│   │   │   │   ├── log.test.ts
│   │   │   │   ├── module.test.ts
│   │   │   │   ├── process.test.ts
│   │   │   │   ├── timeout.test.ts
│   │   │   │   ├── which.test.ts
│   │   │   │   └── wildcard.test.ts
│   │   │   └── workspace
│   │   │       └── workspace-restore.test.ts
│   │   ├── tsconfig.json
│   │   └── tsfiles.txt
│   ├── plugin
│   │   ├── .gitignore
│   │   ├── package.json
│   │   ├── script
│   │   │   └── publish.ts
│   │   ├── src
│   │   │   ├── example-workspace.ts
│   │   │   ├── example.ts
│   │   │   ├── index.ts
│   │   │   ├── shell.ts
│   │   │   ├── tool.ts
│   │   │   └── tui.ts
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── script
│   │   ├── package.json
│   │   ├── src
│   │   │   └── index.ts
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── sdk
│   │   ├── .gitignore
│   │   ├── js
│   │   │   ├── example
│   │   │   │   └── example.ts
│   │   │   ├── package.json
│   │   │   ├── script
│   │   │   │   ├── build.ts
│   │   │   │   └── publish.ts
│   │   │   ├── src
│   │   │   │   ├── client.ts
│   │   │   │   ├── gen
│   │   │   │   │   ├── client
│   │   │   │   │   │   ├── client.gen.ts
│   │   │   │   │   │   ├── index.ts
│   │   │   │   │   │   ├── types.gen.ts
│   │   │   │   │   │   └── utils.gen.ts
│   │   │   │   │   ├── client.gen.ts
│   │   │   │   │   ├── core
│   │   │   │   │   │   ├── auth.gen.ts
│   │   │   │   │   │   ├── bodySerializer.gen.ts
│   │   │   │   │   │   ├── params.gen.ts
│   │   │   │   │   │   ├── pathSerializer.gen.ts
│   │   │   │   │   │   ├── queryKeySerializer.gen.ts
│   │   │   │   │   │   ├── serverSentEvents.gen.ts
│   │   │   │   │   │   ├── types.gen.ts
│   │   │   │   │   │   └── utils.gen.ts
│   │   │   │   │   ├── sdk.gen.ts
│   │   │   │   │   └── types.gen.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── process.ts
│   │   │   │   ├── server.ts
│   │   │   │   └── v2
│   │   │   │       ├── client.ts
│   │   │   │       ├── data.ts
│   │   │   │       ├── gen
│   │   │   │       │   ├── client
│   │   │   │       │   │   ├── client.gen.ts
│   │   │   │       │   │   ├── index.ts
│   │   │   │       │   │   ├── types.gen.ts
│   │   │   │       │   │   └── utils.gen.ts
│   │   │   │       │   ├── client.gen.ts
│   │   │   │       │   ├── core
│   │   │   │       │   │   ├── auth.gen.ts
│   │   │   │       │   │   ├── bodySerializer.gen.ts
│   │   │   │       │   │   ├── params.gen.ts
│   │   │   │       │   │   ├── pathSerializer.gen.ts
│   │   │   │       │   │   ├── queryKeySerializer.gen.ts
│   │   │   │       │   │   ├── serverSentEvents.gen.ts
│   │   │   │       │   │   ├── types.gen.ts
│   │   │   │       │   │   └── utils.gen.ts
│   │   │   │       │   ├── sdk.gen.ts
│   │   │   │       │   └── types.gen.ts
│   │   │   │       ├── index.ts
│   │   │   │       └── server.ts
│   │   │   ├── sst-env.d.ts
│   │   │   ├── tsconfig.json
│   │   │   └── tsconfig.tsbuildinfo
│   │   └── openapi.json
│   ├── shared
│   │   ├── package.json
│   │   ├── src
│   │   │   ├── filesystem.ts
│   │   │   ├── global.ts
│   │   │   ├── types.d.ts
│   │   │   └── util
│   │   │       ├── array.ts
│   │   │       ├── binary.ts
│   │   │       ├── effect-flock.ts
│   │   │       ├── encode.ts
│   │   │       ├── error.ts
│   │   │       ├── flock.ts
│   │   │       ├── fn.ts
│   │   │       ├── glob.ts
│   │   │       ├── hash.ts
│   │   │       ├── identifier.ts
│   │   │       ├── iife.ts
│   │   │       ├── lazy.ts
│   │   │       ├── module.ts
│   │   │       ├── path.ts
│   │   │       ├── retry.ts
│   │   │       └── slug.ts
│   │   ├── sst-env.d.ts
│   │   ├── test
│   │   │   ├── filesystem
│   │   │   │   └── filesystem.test.ts
│   │   │   ├── fixture
│   │   │   │   ├── effect-flock-worker.ts
│   │   │   │   └── flock-worker.ts
│   │   │   ├── lib
│   │   │   │   └── effect.ts
│   │   │   └── util
│   │   │       ├── effect-flock.test.ts
│   │   │       └── flock.test.ts
│   │   └── tsconfig.json
│   ├── slack
│   │   ├── .env.example
│   │   ├── .gitignore
│   │   ├── package.json
│   │   ├── README.md
│   │   ├── src
│   │   │   └── index.ts
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── storybook
│   │   ├── .gitignore
│   │   ├── .storybook
│   │   │   ├── main.ts
│   │   │   ├── manager.ts
│   │   │   ├── mocks
│   │   │   │   ├── app
│   │   │   │   │   ├── components
│   │   │   │   │   │   ├── dialog-select-model-unpaid.tsx
│   │   │   │   │   │   └── dialog-select-model.tsx
│   │   │   │   │   ├── context
│   │   │   │   │   │   ├── command.ts
│   │   │   │   │   │   ├── comments.ts
│   │   │   │   │   │   ├── file.ts
│   │   │   │   │   │   ├── global-sync.ts
│   │   │   │   │   │   ├── language.ts
│   │   │   │   │   │   ├── layout.ts
│   │   │   │   │   │   ├── local.ts
│   │   │   │   │   │   ├── permission.ts
│   │   │   │   │   │   ├── platform.ts
│   │   │   │   │   │   ├── prompt.ts
│   │   │   │   │   │   ├── sdk.ts
│   │   │   │   │   │   └── sync.ts
│   │   │   │   │   └── hooks
│   │   │   │   │       └── use-providers.ts
│   │   │   │   └── solid-router.tsx
│   │   │   ├── playground-css-plugin.ts
│   │   │   ├── preview.tsx
│   │   │   └── theme-tool.ts
│   │   ├── debug-storybook.log
│   │   ├── package.json
│   │   ├── sst-env.d.ts
│   │   └── tsconfig.json
│   ├── ui
│   │   ├── .gitignore
│   │   ├── package.json
│   │   ├── script
│   │   │   ├── colors.txt
│   │   │   └── tailwind.ts
│   │   ├── src
│   │   │   ├── assets
│   │   │   │   ├── audio
│   │   │   │   │   ├── alert-01.aac
│   │   │   │   │   ├── alert-02.aac
│   │   │   │   │   ├── alert-03.aac
│   │   │   │   │   ├── alert-04.aac
│   │   │   │   │   ├── alert-05.aac
│   │   │   │   │   ├── alert-06.aac
│   │   │   │   │   ├── alert-07.aac
│   │   │   │   │   ├── alert-08.aac
│   │   │   │   │   ├── alert-09.aac
│   │   │   │   │   ├── alert-10.aac
│   │   │   │   │   ├── bip-bop-01.aac
│   │   │   │   │   ├── bip-bop-02.aac
│   │   │   │   │   ├── bip-bop-03.aac
│   │   │   │   │   ├── bip-bop-04.aac
│   │   │   │   │   ├── bip-bop-05.aac
│   │   │   │   │   ├── bip-bop-06.aac
│   │   │   │   │   ├── bip-bop-07.aac
│   │   │   │   │   ├── bip-bop-08.aac
│   │   │   │   │   ├── bip-bop-09.aac
│   │   │   │   │   ├── bip-bop-10.aac
│   │   │   │   │   ├── nope-01.aac
│   │   │   │   │   ├── nope-02.aac
│   │   │   │   │   ├── nope-03.aac
│   │   │   │   │   ├── nope-04.aac
│   │   │   │   │   ├── nope-05.aac
│   │   │   │   │   ├── nope-06.aac
│   │   │   │   │   ├── nope-07.aac
│   │   │   │   │   ├── nope-08.aac
│   │   │   │   │   ├── nope-09.aac
│   │   │   │   │   ├── nope-10.aac
│   │   │   │   │   ├── nope-11.aac
│   │   │   │   │   ├── nope-12.aac
│   │   │   │   │   ├── staplebops-01.aac
│   │   │   │   │   ├── staplebops-02.aac
│   │   │   │   │   ├── staplebops-03.aac
│   │   │   │   │   ├── staplebops-04.aac
│   │   │   │   │   ├── staplebops-05.aac
│   │   │   │   │   ├── staplebops-06.aac
│   │   │   │   │   ├── staplebops-07.aac
│   │   │   │   │   ├── yup-01.aac
│   │   │   │   │   ├── yup-02.aac
│   │   │   │   │   ├── yup-03.aac
│   │   │   │   │   ├── yup-04.aac
│   │   │   │   │   ├── yup-05.aac
│   │   │   │   │   └── yup-06.aac
│   │   │   │   ├── favicon
│   │   │   │   │   ├── apple-touch-icon-v3.png
│   │   │   │   │   ├── apple-touch-icon.png
│   │   │   │   │   ├── favicon-96x96-v3.png
│   │   │   │   │   ├── favicon-96x96.png
│   │   │   │   │   ├── favicon-v3.ico
│   │   │   │   │   ├── favicon-v3.svg
│   │   │   │   │   ├── favicon.ico
│   │   │   │   │   ├── favicon.svg
│   │   │   │   │   ├── site.webmanifest
│   │   │   │   │   ├── web-app-manifest-192x192.png
│   │   │   │   │   └── web-app-manifest-512x512.png
│   │   │   │   ├── icons
│   │   │   │   │   ├── app
│   │   │   │   │   │   ├── android-studio.svg
│   │   │   │   │   │   ├── antigravity.svg
│   │   │   │   │   │   ├── cursor.svg
│   │   │   │   │   │   ├── file-explorer.svg
│   │   │   │   │   │   ├── finder.png
│   │   │   │   │   │   ├── ghostty.svg
│   │   │   │   │   │   ├── iterm2.svg
│   │   │   │   │   │   ├── powershell.svg
│   │   │   │   │   │   ├── sublimetext.svg
│   │   │   │   │   │   ├── terminal.png
│   │   │   │   │   │   ├── textmate.png
│   │   │   │   │   │   ├── vscode.svg
│   │   │   │   │   │   ├── warp.png
│   │   │   │   │   │   ├── xcode.png
│   │   │   │   │   │   ├── zed-dark.svg
│   │   │   │   │   │   └── zed.svg
│   │   │   │   │   ├── file-types
│   │   │   │   │   │   ├── 3d.svg
│   │   │   │   │   │   ├── abap.svg
│   │   │   │   │   │   ├── abc.svg
│   │   │   │   │   │   ├── actionscript.svg
│   │   │   │   │   │   ├── ada.svg
│   │   │   │   │   │   ├── adobe-illustrator.svg
│   │   │   │   │   │   ├── adobe-illustrator_light.svg
│   │   │   │   │   │   ├── adobe-photoshop.svg
│   │   │   │   │   │   ├── adobe-photoshop_light.svg
│   │   │   │   │   │   ├── adobe-swc.svg
│   │   │   │   │   │   ├── adonis.svg
│   │   │   │   │   │   ├── advpl.svg
│   │   │   │   │   │   ├── amplify.svg
│   │   │   │   │   │   ├── android.svg
│   │   │   │   │   │   ├── angular.svg
│   │   │   │   │   │   ├── antlr.svg
│   │   │   │   │   │   ├── apiblueprint.svg
│   │   │   │   │   │   ├── apollo.svg
│   │   │   │   │   │   ├── applescript.svg
│   │   │   │   │   │   ├── apps-script.svg
│   │   │   │   │   │   ├── appveyor.svg
│   │   │   │   │   │   ├── architecture.svg
│   │   │   │   │   │   ├── arduino.svg
│   │   │   │   │   │   ├── asciidoc.svg
│   │   │   │   │   │   ├── assembly.svg
│   │   │   │   │   │   ├── astro-config.svg
│   │   │   │   │   │   ├── astro.svg
│   │   │   │   │   │   ├── astyle.svg
│   │   │   │   │   │   ├── audio.svg
│   │   │   │   │   │   ├── aurelia.svg
│   │   │   │   │   │   ├── authors.svg
│   │   │   │   │   │   ├── auto.svg
│   │   │   │   │   │   ├── autohotkey.svg
│   │   │   │   │   │   ├── autoit.svg
│   │   │   │   │   │   ├── auto_light.svg
│   │   │   │   │   │   ├── azure-pipelines.svg
│   │   │   │   │   │   ├── azure.svg
│   │   │   │   │   │   ├── babel.svg
│   │   │   │   │   │   ├── ballerina.svg
│   │   │   │   │   │   ├── bazel.svg
│   │   │   │   │   │   ├── bbx.svg
│   │   │   │   │   │   ├── beancount.svg
│   │   │   │   │   │   ├── bench-js.svg
│   │   │   │   │   │   ├── bench-jsx.svg
│   │   │   │   │   │   ├── bench-ts.svg
│   │   │   │   │   │   ├── bibliography.svg
│   │   │   │   │   │   ├── bibtex-style.svg
│   │   │   │   │   │   ├── bicep.svg
│   │   │   │   │   │   ├── biome.svg
│   │   │   │   │   │   ├── bitbucket.svg
│   │   │   │   │   │   ├── bithound.svg
│   │   │   │   │   │   ├── blender.svg
│   │   │   │   │   │   ├── blink.svg
│   │   │   │   │   │   ├── blink_light.svg
│   │   │   │   │   │   ├── blitz.svg
│   │   │   │   │   │   ├── bower.svg
│   │   │   │   │   │   ├── brainfuck.svg
│   │   │   │   │   │   ├── browserlist.svg
│   │   │   │   │   │   ├── browserlist_light.svg
│   │   │   │   │   │   ├── bruno.svg
│   │   │   │   │   │   ├── buck.svg
│   │   │   │   │   │   ├── bucklescript.svg
│   │   │   │   │   │   ├── buildkite.svg
│   │   │   │   │   │   ├── bun.svg
│   │   │   │   │   │   ├── bun_light.svg
│   │   │   │   │   │   ├── c.svg
│   │   │   │   │   │   ├── c3.svg
│   │   │   │   │   │   ├── cabal.svg
│   │   │   │   │   │   ├── caddy.svg
│   │   │   │   │   │   ├── cadence.svg
│   │   │   │   │   │   ├── cairo.svg
│   │   │   │   │   │   ├── cake.svg
│   │   │   │   │   │   ├── capacitor.svg
│   │   │   │   │   │   ├── capnp.svg
│   │   │   │   │   │   ├── cbx.svg
│   │   │   │   │   │   ├── cds.svg
│   │   │   │   │   │   ├── certificate.svg
│   │   │   │   │   │   ├── changelog.svg
│   │   │   │   │   │   ├── chess.svg
│   │   │   │   │   │   ├── chess_light.svg
│   │   │   │   │   │   ├── chrome.svg
│   │   │   │   │   │   ├── circleci.svg
│   │   │   │   │   │   ├── circleci_light.svg
│   │   │   │   │   │   ├── citation.svg
│   │   │   │   │   │   ├── clangd.svg
│   │   │   │   │   │   ├── claude.svg
│   │   │   │   │   │   ├── cline.svg
│   │   │   │   │   │   ├── clojure.svg
│   │   │   │   │   │   ├── cloudfoundry.svg
│   │   │   │   │   │   ├── cmake.svg
│   │   │   │   │   │   ├── coala.svg
│   │   │   │   │   │   ├── cobol.svg
│   │   │   │   │   │   ├── coconut.svg
│   │   │   │   │   │   ├── code-climate.svg
│   │   │   │   │   │   ├── code-climate_light.svg
│   │   │   │   │   │   ├── codecov.svg
│   │   │   │   │   │   ├── codeowners.svg
│   │   │   │   │   │   ├── coderabbit-ai.svg
│   │   │   │   │   │   ├── coffee.svg
│   │   │   │   │   │   ├── coldfusion.svg
│   │   │   │   │   │   ├── coloredpetrinets.svg
│   │   │   │   │   │   ├── command.svg
│   │   │   │   │   │   ├── commitizen.svg
│   │   │   │   │   │   ├── commitlint.svg
│   │   │   │   │   │   ├── concourse.svg
│   │   │   │   │   │   ├── conduct.svg
│   │   │   │   │   │   ├── console.svg
│   │   │   │   │   │   ├── contentlayer.svg
│   │   │   │   │   │   ├── context.svg
│   │   │   │   │   │   ├── contributing.svg
│   │   │   │   │   │   ├── controller.svg
│   │   │   │   │   │   ├── copilot.svg
│   │   │   │   │   │   ├── copilot_light.svg
│   │   │   │   │   │   ├── cpp.svg
│   │   │   │   │   │   ├── craco.svg
│   │   │   │   │   │   ├── credits.svg
│   │   │   │   │   │   ├── crystal.svg
│   │   │   │   │   │   ├── crystal_light.svg
│   │   │   │   │   │   ├── csharp.svg
│   │   │   │   │   │   ├── css-map.svg
│   │   │   │   │   │   ├── css.svg
│   │   │   │   │   │   ├── cucumber.svg
│   │   │   │   │   │   ├── cuda.svg
│   │   │   │   │   │   ├── cursor.svg
│   │   │   │   │   │   ├── cursor_light.svg
│   │   │   │   │   │   ├── cypress.svg
│   │   │   │   │   │   ├── d.svg
│   │   │   │   │   │   ├── dart.svg
│   │   │   │   │   │   ├── dart_generated.svg
│   │   │   │   │   │   ├── database.svg
│   │   │   │   │   │   ├── deepsource.svg
│   │   │   │   │   │   ├── denizenscript.svg
│   │   │   │   │   │   ├── deno.svg
│   │   │   │   │   │   ├── deno_light.svg
│   │   │   │   │   │   ├── dependabot.svg
│   │   │   │   │   │   ├── dependencies-update.svg
│   │   │   │   │   │   ├── dhall.svg
│   │   │   │   │   │   ├── diff.svg
│   │   │   │   │   │   ├── dinophp.svg
│   │   │   │   │   │   ├── disc.svg
│   │   │   │   │   │   ├── django.svg
│   │   │   │   │   │   ├── dll.svg
│   │   │   │   │   │   ├── docker.svg
│   │   │   │   │   │   ├── doctex-installer.svg
│   │   │   │   │   │   ├── document.svg
│   │   │   │   │   │   ├── dotjs.svg
│   │   │   │   │   │   ├── drawio.svg
│   │   │   │   │   │   ├── drizzle.svg
│   │   │   │   │   │   ├── drone.svg
│   │   │   │   │   │   ├── drone_light.svg
│   │   │   │   │   │   ├── duc.svg
│   │   │   │   │   │   ├── dune.svg
│   │   │   │   │   │   ├── edge.svg
│   │   │   │   │   │   ├── editorconfig.svg
│   │   │   │   │   │   ├── ejs.svg
│   │   │   │   │   │   ├── elixir.svg
│   │   │   │   │   │   ├── elm.svg
│   │   │   │   │   │   ├── email.svg
│   │   │   │   │   │   ├── ember.svg
│   │   │   │   │   │   ├── epub.svg
│   │   │   │   │   │   ├── erlang.svg
│   │   │   │   │   │   ├── esbuild.svg
│   │   │   │   │   │   ├── eslint.svg
│   │   │   │   │   │   ├── excalidraw.svg
│   │   │   │   │   │   ├── exe.svg
│   │   │   │   │   │   ├── fastlane.svg
│   │   │   │   │   │   ├── favicon.svg
│   │   │   │   │   │   ├── figma.svg
│   │   │   │   │   │   ├── firebase.svg
│   │   │   │   │   │   ├── flash.svg
│   │   │   │   │   │   ├── flow.svg
│   │   │   │   │   │   ├── folder-admin-open.svg
│   │   │   │   │   │   ├── folder-admin.svg
│   │   │   │   │   │   ├── folder-android-open.svg
│   │   │   │   │   │   ├── folder-android.svg
│   │   │   │   │   │   ├── folder-angular-open.svg
│   │   │   │   │   │   ├── folder-angular.svg
│   │   │   │   │   │   ├── folder-animation-open.svg
│   │   │   │   │   │   ├── folder-animation.svg
│   │   │   │   │   │   ├── folder-ansible-open.svg
│   │   │   │   │   │   ├── folder-ansible.svg
│   │   │   │   │   │   ├── folder-api-open.svg
│   │   │   │   │   │   ├── folder-api.svg
│   │   │   │   │   │   ├── folder-apollo-open.svg
│   │   │   │   │   │   ├── folder-apollo.svg
│   │   │   │   │   │   ├── folder-app-open.svg
│   │   │   │   │   │   ├── folder-app.svg
│   │   │   │   │   │   ├── folder-archive-open.svg
│   │   │   │   │   │   ├── folder-archive.svg
│   │   │   │   │   │   ├── folder-astro-open.svg
│   │   │   │   │   │   ├── folder-astro.svg
│   │   │   │   │   │   ├── folder-atom-open.svg
│   │   │   │   │   │   ├── folder-atom.svg
│   │   │   │   │   │   ├── folder-attachment-open.svg
│   │   │   │   │   │   ├── folder-attachment.svg
│   │   │   │   │   │   ├── folder-audio-open.svg
│   │   │   │   │   │   ├── folder-audio.svg
│   │   │   │   │   │   ├── folder-aurelia-open.svg
│   │   │   │   │   │   ├── folder-aurelia.svg
│   │   │   │   │   │   ├── folder-aws-open.svg
│   │   │   │   │   │   ├── folder-aws.svg
│   │   │   │   │   │   ├── folder-azure-pipelines-open.svg
│   │   │   │   │   │   ├── folder-azure-pipelines.svg
│   │   │   │   │   │   ├── folder-backup-open.svg
│   │   │   │   │   │   ├── folder-backup.svg
│   │   │   │   │   │   ├── folder-base-open.svg
│   │   │   │   │   │   ├── folder-base.svg
│   │   │   │   │   │   ├── folder-batch-open.svg
│   │   │   │   │   │   ├── folder-batch.svg
│   │   │   │   │   │   ├── folder-benchmark-open.svg
│   │   │   │   │   │   ├── folder-benchmark.svg
│   │   │   │   │   │   ├── folder-bibliography-open.svg
│   │   │   │   │   │   ├── folder-bibliography.svg
│   │   │   │   │   │   ├── folder-bicep-open.svg
│   │   │   │   │   │   ├── folder-bicep.svg
│   │   │   │   │   │   ├── folder-blender-open.svg
│   │   │   │   │   │   ├── folder-blender.svg
│   │   │   │   │   │   ├── folder-bloc-open.svg
│   │   │   │   │   │   ├── folder-bloc.svg
│   │   │   │   │   │   ├── folder-bower-open.svg
│   │   │   │   │   │   ├── folder-bower.svg
│   │   │   │   │   │   ├── folder-buildkite-open.svg
│   │   │   │   │   │   ├── folder-buildkite.svg
│   │   │   │   │   │   ├── folder-cart-open.svg
│   │   │   │   │   │   ├── folder-cart.svg
│   │   │   │   │   │   ├── folder-changesets-open.svg
│   │   │   │   │   │   ├── folder-changesets.svg
│   │   │   │   │   │   ├── folder-ci-open.svg
│   │   │   │   │   │   ├── folder-ci.svg
│   │   │   │   │   │   ├── folder-circleci-open.svg
│   │   │   │   │   │   ├── folder-circleci.svg
│   │   │   │   │   │   ├── folder-class-open.svg
│   │   │   │   │   │   ├── folder-class.svg
│   │   │   │   │   │   ├── folder-claude-open.svg
│   │   │   │   │   │   ├── folder-claude.svg
│   │   │   │   │   │   ├── folder-client-open.svg
│   │   │   │   │   │   ├── folder-client.svg
│   │   │   │   │   │   ├── folder-cline-open.svg
│   │   │   │   │   │   ├── folder-cline.svg
│   │   │   │   │   │   ├── folder-cloud-functions-open.svg
│   │   │   │   │   │   ├── folder-cloud-functions.svg
│   │   │   │   │   │   ├── folder-cloudflare-open.svg
│   │   │   │   │   │   ├── folder-cloudflare.svg
│   │   │   │   │   │   ├── folder-cluster-open.svg
│   │   │   │   │   │   ├── folder-cluster.svg
│   │   │   │   │   │   ├── folder-cobol-open.svg
│   │   │   │   │   │   ├── folder-cobol.svg
│   │   │   │   │   │   ├── folder-command-open.svg
│   │   │   │   │   │   ├── folder-command.svg
│   │   │   │   │   │   ├── folder-components-open.svg
│   │   │   │   │   │   ├── folder-components.svg
│   │   │   │   │   │   ├── folder-config-open.svg
│   │   │   │   │   │   ├── folder-config.svg
│   │   │   │   │   │   ├── folder-connection-open.svg
│   │   │   │   │   │   ├── folder-connection.svg
│   │   │   │   │   │   ├── folder-console-open.svg
│   │   │   │   │   │   ├── folder-console.svg
│   │   │   │   │   │   ├── folder-constant-open.svg
│   │   │   │   │   │   ├── folder-constant.svg
│   │   │   │   │   │   ├── folder-container-open.svg
│   │   │   │   │   │   ├── folder-container.svg
│   │   │   │   │   │   ├── folder-content-open.svg
│   │   │   │   │   │   ├── folder-content.svg
│   │   │   │   │   │   ├── folder-context-open.svg
│   │   │   │   │   │   ├── folder-context.svg
│   │   │   │   │   │   ├── folder-contract-open.svg
│   │   │   │   │   │   ├── folder-contract.svg
│   │   │   │   │   │   ├── folder-controller-open.svg
│   │   │   │   │   │   ├── folder-controller.svg
│   │   │   │   │   │   ├── folder-core-open.svg
│   │   │   │   │   │   ├── folder-core.svg
│   │   │   │   │   │   ├── folder-coverage-open.svg
│   │   │   │   │   │   ├── folder-coverage.svg
│   │   │   │   │   │   ├── folder-css-open.svg
│   │   │   │   │   │   ├── folder-css.svg
│   │   │   │   │   │   ├── folder-cursor-open.svg
│   │   │   │   │   │   ├── folder-cursor-open_light.svg
│   │   │   │   │   │   ├── folder-cursor.svg
│   │   │   │   │   │   ├── folder-cursor_light.svg
│   │   │   │   │   │   ├── folder-custom-open.svg
│   │   │   │   │   │   ├── folder-custom.svg
│   │   │   │   │   │   ├── folder-cypress-open.svg
│   │   │   │   │   │   ├── folder-cypress.svg
│   │   │   │   │   │   ├── folder-dart-open.svg
│   │   │   │   │   │   ├── folder-dart.svg
│   │   │   │   │   │   ├── folder-database-open.svg
│   │   │   │   │   │   ├── folder-database.svg
│   │   │   │   │   │   ├── folder-debug-open.svg
│   │   │   │   │   │   ├── folder-debug.svg
│   │   │   │   │   │   ├── folder-decorators-open.svg
│   │   │   │   │   │   ├── folder-decorators.svg
│   │   │   │   │   │   ├── folder-delta-open.svg
│   │   │   │   │   │   ├── folder-delta.svg
│   │   │   │   │   │   ├── folder-desktop-open.svg
│   │   │   │   │   │   ├── folder-desktop.svg
│   │   │   │   │   │   ├── folder-directive-open.svg
│   │   │   │   │   │   ├── folder-directive.svg
│   │   │   │   │   │   ├── folder-dist-open.svg
│   │   │   │   │   │   ├── folder-dist.svg
│   │   │   │   │   │   ├── folder-docker-open.svg
│   │   │   │   │   │   ├── folder-docker.svg
│   │   │   │   │   │   ├── folder-docs-open.svg
│   │   │   │   │   │   ├── folder-docs.svg
│   │   │   │   │   │   ├── folder-download-open.svg
│   │   │   │   │   │   ├── folder-download.svg
│   │   │   │   │   │   ├── folder-drizzle-open.svg
│   │   │   │   │   │   ├── folder-drizzle.svg
│   │   │   │   │   │   ├── folder-dump-open.svg
│   │   │   │   │   │   ├── folder-dump.svg
│   │   │   │   │   │   ├── folder-element-open.svg
│   │   │   │   │   │   ├── folder-element.svg
│   │   │   │   │   │   ├── folder-enum-open.svg
│   │   │   │   │   │   ├── folder-enum.svg
│   │   │   │   │   │   ├── folder-environment-open.svg
│   │   │   │   │   │   ├── folder-environment.svg
│   │   │   │   │   │   ├── folder-error-open.svg
│   │   │   │   │   │   ├── folder-error.svg
│   │   │   │   │   │   ├── folder-event-open.svg
│   │   │   │   │   │   ├── folder-event.svg
│   │   │   │   │   │   ├── folder-examples-open.svg
│   │   │   │   │   │   ├── folder-examples.svg
│   │   │   │   │   │   ├── folder-expo-open.svg
│   │   │   │   │   │   ├── folder-expo.svg
│   │   │   │   │   │   ├── folder-export-open.svg
│   │   │   │   │   │   ├── folder-export.svg
│   │   │   │   │   │   ├── folder-fastlane-open.svg
│   │   │   │   │   │   ├── folder-fastlane.svg
│   │   │   │   │   │   ├── folder-favicon-open.svg
│   │   │   │   │   │   ├── folder-favicon.svg
│   │   │   │   │   │   ├── folder-firebase-open.svg
│   │   │   │   │   │   ├── folder-firebase.svg
│   │   │   │   │   │   ├── folder-firestore-open.svg
│   │   │   │   │   │   ├── folder-firestore.svg
│   │   │   │   │   │   ├── folder-flow-open.svg
│   │   │   │   │   │   ├── folder-flow.svg
│   │   │   │   │   │   ├── folder-flutter-open.svg
│   │   │   │   │   │   ├── folder-flutter.svg
│   │   │   │   │   │   ├── folder-font-open.svg
│   │   │   │   │   │   ├── folder-font.svg
│   │   │   │   │   │   ├── folder-forgejo-open.svg
│   │   │   │   │   │   ├── folder-forgejo.svg
│   │   │   │   │   │   ├── folder-functions-open.svg
│   │   │   │   │   │   ├── folder-functions.svg
│   │   │   │   │   │   ├── folder-gamemaker-open.svg
│   │   │   │   │   │   ├── folder-gamemaker.svg
│   │   │   │   │   │   ├── folder-generator-open.svg
│   │   │   │   │   │   ├── folder-generator.svg
│   │   │   │   │   │   ├── folder-gh-workflows-open.svg
│   │   │   │   │   │   ├── folder-gh-workflows.svg
│   │   │   │   │   │   ├── folder-git-open.svg
│   │   │   │   │   │   ├── folder-git.svg
│   │   │   │   │   │   ├── folder-gitea-open.svg
│   │   │   │   │   │   ├── folder-gitea.svg
│   │   │   │   │   │   ├── folder-github-open.svg
│   │   │   │   │   │   ├── folder-github.svg
│   │   │   │   │   │   ├── folder-gitlab-open.svg
│   │   │   │   │   │   ├── folder-gitlab.svg
│   │   │   │   │   │   ├── folder-global-open.svg
│   │   │   │   │   │   ├── folder-global.svg
│   │   │   │   │   │   ├── folder-godot-open.svg
│   │   │   │   │   │   ├── folder-godot.svg
│   │   │   │   │   │   ├── folder-gradle-open.svg
│   │   │   │   │   │   ├── folder-gradle.svg
│   │   │   │   │   │   ├── folder-graphql-open.svg
│   │   │   │   │   │   ├── folder-graphql.svg
│   │   │   │   │   │   ├── folder-guard-open.svg
│   │   │   │   │   │   ├── folder-guard.svg
│   │   │   │   │   │   ├── folder-gulp-open.svg
│   │   │   │   │   │   ├── folder-gulp.svg
│   │   │   │   │   │   ├── folder-helm-open.svg
│   │   │   │   │   │   ├── folder-helm.svg
│   │   │   │   │   │   ├── folder-helper-open.svg
│   │   │   │   │   │   ├── folder-helper.svg
│   │   │   │   │   │   ├── folder-home-open.svg
│   │   │   │   │   │   ├── folder-home.svg
│   │   │   │   │   │   ├── folder-hook-open.svg
│   │   │   │   │   │   ├── folder-hook.svg
│   │   │   │   │   │   ├── folder-husky-open.svg
│   │   │   │   │   │   ├── folder-husky.svg
│   │   │   │   │   │   ├── folder-i18n-open.svg
│   │   │   │   │   │   ├── folder-i18n.svg
│   │   │   │   │   │   ├── folder-images-open.svg
│   │   │   │   │   │   ├── folder-images.svg
│   │   │   │   │   │   ├── folder-import-open.svg
│   │   │   │   │   │   ├── folder-import.svg
│   │   │   │   │   │   ├── folder-include-open.svg
│   │   │   │   │   │   ├── folder-include.svg
│   │   │   │   │   │   ├── folder-intellij-open.svg
│   │   │   │   │   │   ├── folder-intellij-open_light.svg
│   │   │   │   │   │   ├── folder-intellij.svg
│   │   │   │   │   │   ├── folder-intellij_light.svg
│   │   │   │   │   │   ├── folder-interceptor-open.svg
│   │   │   │   │   │   ├── folder-interceptor.svg
│   │   │   │   │   │   ├── folder-interface-open.svg
│   │   │   │   │   │   ├── folder-interface.svg
│   │   │   │   │   │   ├── folder-ios-open.svg
│   │   │   │   │   │   ├── folder-ios.svg
│   │   │   │   │   │   ├── folder-java-open.svg
│   │   │   │   │   │   ├── folder-java.svg
│   │   │   │   │   │   ├── folder-javascript-open.svg
│   │   │   │   │   │   ├── folder-javascript.svg
│   │   │   │   │   │   ├── folder-jinja-open.svg
│   │   │   │   │   │   ├── folder-jinja-open_light.svg
│   │   │   │   │   │   ├── folder-jinja.svg
│   │   │   │   │   │   ├── folder-jinja_light.svg
│   │   │   │   │   │   ├── folder-job-open.svg
│   │   │   │   │   │   ├── folder-job.svg
│   │   │   │   │   │   ├── folder-json-open.svg
│   │   │   │   │   │   ├── folder-json.svg
│   │   │   │   │   │   ├── folder-jupyter-open.svg
│   │   │   │   │   │   ├── folder-jupyter.svg
│   │   │   │   │   │   ├── folder-keys-open.svg
│   │   │   │   │   │   ├── folder-keys.svg
│   │   │   │   │   │   ├── folder-kubernetes-open.svg
│   │   │   │   │   │   ├── folder-kubernetes.svg
│   │   │   │   │   │   ├── folder-kusto-open.svg
│   │   │   │   │   │   ├── folder-kusto.svg
│   │   │   │   │   │   ├── folder-layout-open.svg
│   │   │   │   │   │   ├── folder-layout.svg
│   │   │   │   │   │   ├── folder-lefthook-open.svg
│   │   │   │   │   │   ├── folder-lefthook.svg
│   │   │   │   │   │   ├── folder-less-open.svg
│   │   │   │   │   │   ├── folder-less.svg
│   │   │   │   │   │   ├── folder-lib-open.svg
│   │   │   │   │   │   ├── folder-lib.svg
│   │   │   │   │   │   ├── folder-link-open.svg
│   │   │   │   │   │   ├── folder-link.svg
│   │   │   │   │   │   ├── folder-linux-open.svg
│   │   │   │   │   │   ├── folder-linux.svg
│   │   │   │   │   │   ├── folder-liquibase-open.svg
│   │   │   │   │   │   ├── folder-liquibase.svg
│   │   │   │   │   │   ├── folder-log-open.svg
│   │   │   │   │   │   ├── folder-log.svg
│   │   │   │   │   │   ├── folder-lottie-open.svg
│   │   │   │   │   │   ├── folder-lottie.svg
│   │   │   │   │   │   ├── folder-lua-open.svg
│   │   │   │   │   │   ├── folder-lua.svg
│   │   │   │   │   │   ├── folder-luau-open.svg
│   │   │   │   │   │   ├── folder-luau.svg
│   │   │   │   │   │   ├── folder-macos-open.svg
│   │   │   │   │   │   ├── folder-macos.svg
│   │   │   │   │   │   ├── folder-mail-open.svg
│   │   │   │   │   │   ├── folder-mail.svg
│   │   │   │   │   │   ├── folder-mappings-open.svg
│   │   │   │   │   │   ├── folder-mappings.svg
│   │   │   │   │   │   ├── folder-markdown-open.svg
│   │   │   │   │   │   ├── folder-markdown.svg
│   │   │   │   │   │   ├── folder-mercurial-open.svg
│   │   │   │   │   │   ├── folder-mercurial.svg
│   │   │   │   │   │   ├── folder-messages-open.svg
│   │   │   │   │   │   ├── folder-messages.svg
│   │   │   │   │   │   ├── folder-meta-open.svg
│   │   │   │   │   │   ├── folder-meta.svg
│   │   │   │   │   │   ├── folder-middleware-open.svg
│   │   │   │   │   │   ├── folder-middleware.svg
│   │   │   │   │   │   ├── folder-mjml-open.svg
│   │   │   │   │   │   ├── folder-mjml.svg
│   │   │   │   │   │   ├── folder-mobile-open.svg
│   │   │   │   │   │   ├── folder-mobile.svg
│   │   │   │   │   │   ├── folder-mock-open.svg
│   │   │   │   │   │   ├── folder-mock.svg
│   │   │   │   │   │   ├── folder-mojo-open.svg
│   │   │   │   │   │   ├── folder-mojo.svg
│   │   │   │   │   │   ├── folder-molecule-open.svg
│   │   │   │   │   │   ├── folder-molecule.svg
│   │   │   │   │   │   ├── folder-moon-open.svg
│   │   │   │   │   │   ├── folder-moon.svg
│   │   │   │   │   │   ├── folder-netlify-open.svg
│   │   │   │   │   │   ├── folder-netlify.svg
│   │   │   │   │   │   ├── folder-next-open.svg
│   │   │   │   │   │   ├── folder-next.svg
│   │   │   │   │   │   ├── folder-ngrx-store-open.svg
│   │   │   │   │   │   ├── folder-ngrx-store.svg
│   │   │   │   │   │   ├── folder-node-open.svg
│   │   │   │   │   │   ├── folder-node.svg
│   │   │   │   │   │   ├── folder-nuxt-open.svg
│   │   │   │   │   │   ├── folder-nuxt.svg
│   │   │   │   │   │   ├── folder-obsidian-open.svg
│   │   │   │   │   │   ├── folder-obsidian.svg
│   │   │   │   │   │   ├── folder-open.svg
│   │   │   │   │   │   ├── folder-organism-open.svg
│   │   │   │   │   │   ├── folder-organism.svg
│   │   │   │   │   │   ├── folder-other-open.svg
│   │   │   │   │   │   ├── folder-other.svg
│   │   │   │   │   │   ├── folder-packages-open.svg
│   │   │   │   │   │   ├── folder-packages.svg
│   │   │   │   │   │   ├── folder-pdf-open.svg
│   │   │   │   │   │   ├── folder-pdf.svg
│   │   │   │   │   │   ├── folder-pdm-open.svg
│   │   │   │   │   │   ├── folder-pdm.svg
│   │   │   │   │   │   ├── folder-php-open.svg
│   │   │   │   │   │   ├── folder-php.svg
│   │   │   │   │   │   ├── folder-phpmailer-open.svg
│   │   │   │   │   │   ├── folder-phpmailer.svg
│   │   │   │   │   │   ├── folder-pipe-open.svg
│   │   │   │   │   │   ├── folder-pipe.svg
│   │   │   │   │   │   ├── folder-plastic-open.svg
│   │   │   │   │   │   ├── folder-plastic.svg
│   │   │   │   │   │   ├── folder-plugin-open.svg
│   │   │   │   │   │   ├── folder-plugin.svg
│   │   │   │   │   │   ├── folder-policy-open.svg
│   │   │   │   │   │   ├── folder-policy.svg
│   │   │   │   │   │   ├── folder-powershell-open.svg
│   │   │   │   │   │   ├── folder-powershell.svg
│   │   │   │   │   │   ├── folder-prisma-open.svg
│   │   │   │   │   │   ├── folder-prisma.svg
│   │   │   │   │   │   ├── folder-private-open.svg
│   │   │   │   │   │   ├── folder-private.svg
│   │   │   │   │   │   ├── folder-project-open.svg
│   │   │   │   │   │   ├── folder-project.svg
│   │   │   │   │   │   ├── folder-prompts-open.svg
│   │   │   │   │   │   ├── folder-prompts.svg
│   │   │   │   │   │   ├── folder-proto-open.svg
│   │   │   │   │   │   ├── folder-proto.svg
│   │   │   │   │   │   ├── folder-public-open.svg
│   │   │   │   │   │   ├── folder-public.svg
│   │   │   │   │   │   ├── folder-python-open.svg
│   │   │   │   │   │   ├── folder-python.svg
│   │   │   │   │   │   ├── folder-pytorch-open.svg
│   │   │   │   │   │   ├── folder-pytorch.svg
│   │   │   │   │   │   ├── folder-quasar-open.svg
│   │   │   │   │   │   ├── folder-quasar.svg
│   │   │   │   │   │   ├── folder-queue-open.svg
│   │   │   │   │   │   ├── folder-queue.svg
│   │   │   │   │   │   ├── folder-react-components-open.svg
│   │   │   │   │   │   ├── folder-react-components.svg
│   │   │   │   │   │   ├── folder-redux-reducer-open.svg
│   │   │   │   │   │   ├── folder-redux-reducer.svg
│   │   │   │   │   │   ├── folder-repository-open.svg
│   │   │   │   │   │   ├── folder-repository.svg
│   │   │   │   │   │   ├── folder-resolver-open.svg
│   │   │   │   │   │   ├── folder-resolver.svg
│   │   │   │   │   │   ├── folder-resource-open.svg
│   │   │   │   │   │   ├── folder-resource.svg
│   │   │   │   │   │   ├── folder-review-open.svg
│   │   │   │   │   │   ├── folder-review.svg
│   │   │   │   │   │   ├── folder-robot-open.svg
│   │   │   │   │   │   ├── folder-robot.svg
│   │   │   │   │   │   ├── folder-routes-open.svg
│   │   │   │   │   │   ├── folder-routes.svg
│   │   │   │   │   │   ├── folder-rules-open.svg
│   │   │   │   │   │   ├── folder-rules.svg
│   │   │   │   │   │   ├── folder-rust-open.svg
│   │   │   │   │   │   ├── folder-rust.svg
│   │   │   │   │   │   ├── folder-sandbox-open.svg
│   │   │   │   │   │   ├── folder-sandbox.svg
│   │   │   │   │   │   ├── folder-sass-open.svg
│   │   │   │   │   │   ├── folder-sass.svg
│   │   │   │   │   │   ├── folder-scala-open.svg
│   │   │   │   │   │   ├── folder-scala.svg
│   │   │   │   │   │   ├── folder-scons-open.svg
│   │   │   │   │   │   ├── folder-scons.svg
│   │   │   │   │   │   ├── folder-scripts-open.svg
│   │   │   │   │   │   ├── folder-scripts.svg
│   │   │   │   │   │   ├── folder-secure-open.svg
│   │   │   │   │   │   ├── folder-secure.svg
│   │   │   │   │   │   ├── folder-seeders-open.svg
│   │   │   │   │   │   ├── folder-seeders.svg
│   │   │   │   │   │   ├── folder-server-open.svg
│   │   │   │   │   │   ├── folder-server.svg
│   │   │   │   │   │   ├── folder-serverless-open.svg
│   │   │   │   │   │   ├── folder-serverless.svg
│   │   │   │   │   │   ├── folder-shader-open.svg
│   │   │   │   │   │   ├── folder-shader.svg
│   │   │   │   │   │   ├── folder-shared-open.svg
│   │   │   │   │   │   ├── folder-shared.svg
│   │   │   │   │   │   ├── folder-snapcraft-open.svg
│   │   │   │   │   │   ├── folder-snapcraft.svg
│   │   │   │   │   │   ├── folder-snippet-open.svg
│   │   │   │   │   │   ├── folder-snippet.svg
│   │   │   │   │   │   ├── folder-src-open.svg
│   │   │   │   │   │   ├── folder-src-tauri-open.svg
│   │   │   │   │   │   ├── folder-src-tauri.svg
│   │   │   │   │   │   ├── folder-src.svg
│   │   │   │   │   │   ├── folder-stack-open.svg
│   │   │   │   │   │   ├── folder-stack.svg
│   │   │   │   │   │   ├── folder-stencil-open.svg
│   │   │   │   │   │   ├── folder-stencil.svg
│   │   │   │   │   │   ├── folder-store-open.svg
│   │   │   │   │   │   ├── folder-store.svg
│   │   │   │   │   │   ├── folder-storybook-open.svg
│   │   │   │   │   │   ├── folder-storybook.svg
│   │   │   │   │   │   ├── folder-stylus-open.svg
│   │   │   │   │   │   ├── folder-stylus.svg
│   │   │   │   │   │   ├── folder-sublime-open.svg
│   │   │   │   │   │   ├── folder-sublime.svg
│   │   │   │   │   │   ├── folder-supabase-open.svg
│   │   │   │   │   │   ├── folder-supabase.svg
│   │   │   │   │   │   ├── folder-svelte-open.svg
│   │   │   │   │   │   ├── folder-svelte.svg
│   │   │   │   │   │   ├── folder-svg-open.svg
│   │   │   │   │   │   ├── folder-svg.svg
│   │   │   │   │   │   ├── folder-syntax-open.svg
│   │   │   │   │   │   ├── folder-syntax.svg
│   │   │   │   │   │   ├── folder-target-open.svg
│   │   │   │   │   │   ├── folder-target.svg
│   │   │   │   │   │   ├── folder-taskfile-open.svg
│   │   │   │   │   │   ├── folder-taskfile.svg
│   │   │   │   │   │   ├── folder-tasks-open.svg
│   │   │   │   │   │   ├── folder-tasks.svg
│   │   │   │   │   │   ├── folder-television-open.svg
│   │   │   │   │   │   ├── folder-television.svg
│   │   │   │   │   │   ├── folder-temp-open.svg
│   │   │   │   │   │   ├── folder-temp.svg
│   │   │   │   │   │   ├── folder-template-open.svg
│   │   │   │   │   │   ├── folder-template.svg
│   │   │   │   │   │   ├── folder-terraform-open.svg
│   │   │   │   │   │   ├── folder-terraform.svg
│   │   │   │   │   │   ├── folder-test-open.svg
│   │   │   │   │   │   ├── folder-test.svg
│   │   │   │   │   │   ├── folder-theme-open.svg
│   │   │   │   │   │   ├── folder-theme.svg
│   │   │   │   │   │   ├── folder-tools-open.svg
│   │   │   │   │   │   ├── folder-tools.svg
│   │   │   │   │   │   ├── folder-trash-open.svg
│   │   │   │   │   │   ├── folder-trash.svg
│   │   │   │   │   │   ├── folder-trigger-open.svg
│   │   │   │   │   │   ├── folder-trigger.svg
│   │   │   │   │   │   ├── folder-turborepo-open.svg
│   │   │   │   │   │   ├── folder-turborepo.svg
│   │   │   │   │   │   ├── folder-typescript-open.svg
│   │   │   │   │   │   ├── folder-typescript.svg
│   │   │   │   │   │   ├── folder-ui-open.svg
│   │   │   │   │   │   ├── folder-ui.svg
│   │   │   │   │   │   ├── folder-unity-open.svg
│   │   │   │   │   │   ├── folder-unity.svg
│   │   │   │   │   │   ├── folder-update-open.svg
│   │   │   │   │   │   ├── folder-update.svg
│   │   │   │   │   │   ├── folder-upload-open.svg
│   │   │   │   │   │   ├── folder-upload.svg
│   │   │   │   │   │   ├── folder-utils-open.svg
│   │   │   │   │   │   ├── folder-utils.svg
│   │   │   │   │   │   ├── folder-vercel-open.svg
│   │   │   │   │   │   ├── folder-vercel.svg
│   │   │   │   │   │   ├── folder-verdaccio-open.svg
│   │   │   │   │   │   ├── folder-verdaccio.svg
│   │   │   │   │   │   ├── folder-video-open.svg
│   │   │   │   │   │   ├── folder-video.svg
│   │   │   │   │   │   ├── folder-views-open.svg
│   │   │   │   │   │   ├── folder-views.svg
│   │   │   │   │   │   ├── folder-vm-open.svg
│   │   │   │   │   │   ├── folder-vm.svg
│   │   │   │   │   │   ├── folder-vscode-open.svg
│   │   │   │   │   │   ├── folder-vscode.svg
│   │   │   │   │   │   ├── folder-vue-directives-open.svg
│   │   │   │   │   │   ├── folder-vue-directives.svg
│   │   │   │   │   │   ├── folder-vue-open.svg
│   │   │   │   │   │   ├── folder-vue.svg
│   │   │   │   │   │   ├── folder-vuepress-open.svg
│   │   │   │   │   │   ├── folder-vuepress.svg
│   │   │   │   │   │   ├── folder-vuex-store-open.svg
│   │   │   │   │   │   ├── folder-vuex-store.svg
│   │   │   │   │   │   ├── folder-wakatime-open.svg
│   │   │   │   │   │   ├── folder-wakatime.svg
│   │   │   │   │   │   ├── folder-webpack-open.svg
│   │   │   │   │   │   ├── folder-webpack.svg
│   │   │   │   │   │   ├── folder-windows-open.svg
│   │   │   │   │   │   ├── folder-windows.svg
│   │   │   │   │   │   ├── folder-wordpress-open.svg
│   │   │   │   │   │   ├── folder-wordpress.svg
│   │   │   │   │   │   ├── folder-yarn-open.svg
│   │   │   │   │   │   ├── folder-yarn.svg
│   │   │   │   │   │   ├── folder-zeabur-open.svg
│   │   │   │   │   │   ├── folder-zeabur.svg
│   │   │   │   │   │   ├── folder.svg
│   │   │   │   │   │   ├── font.svg
│   │   │   │   │   │   ├── forth.svg
│   │   │   │   │   │   ├── fortran.svg
│   │   │   │   │   │   ├── foxpro.svg
│   │   │   │   │   │   ├── freemarker.svg
│   │   │   │   │   │   ├── fsharp.svg
│   │   │   │   │   │   ├── fusebox.svg
│   │   │   │   │   │   ├── gamemaker.svg
│   │   │   │   │   │   ├── garden.svg
│   │   │   │   │   │   ├── gatsby.svg
│   │   │   │   │   │   ├── gcp.svg
│   │   │   │   │   │   ├── gemfile.svg
│   │   │   │   │   │   ├── gemini-ai.svg
│   │   │   │   │   │   ├── gemini.svg
│   │   │   │   │   │   ├── git.svg
│   │   │   │   │   │   ├── github-actions-workflow.svg
│   │   │   │   │   │   ├── github-sponsors.svg
│   │   │   │   │   │   ├── gitlab.svg
│   │   │   │   │   │   ├── gitpod.svg
│   │   │   │   │   │   ├── gleam.svg
│   │   │   │   │   │   ├── gnuplot.svg
│   │   │   │   │   │   ├── go-mod.svg
│   │   │   │   │   │   ├── go.svg
│   │   │   │   │   │   ├── godot-assets.svg
│   │   │   │   │   │   ├── godot.svg
│   │   │   │   │   │   ├── go_gopher.svg
│   │   │   │   │   │   ├── gradle.svg
│   │   │   │   │   │   ├── grafana-alloy.svg
│   │   │   │   │   │   ├── grain.svg
│   │   │   │   │   │   ├── graphcool.svg
│   │   │   │   │   │   ├── graphql.svg
│   │   │   │   │   │   ├── gridsome.svg
│   │   │   │   │   │   ├── groovy.svg
│   │   │   │   │   │   ├── grunt.svg
│   │   │   │   │   │   ├── gulp.svg
│   │   │   │   │   │   ├── h.svg
│   │   │   │   │   │   ├── hack.svg
│   │   │   │   │   │   ├── hadolint.svg
│   │   │   │   │   │   ├── haml.svg
│   │   │   │   │   │   ├── handlebars.svg
│   │   │   │   │   │   ├── hardhat.svg
│   │   │   │   │   │   ├── harmonix.svg
│   │   │   │   │   │   ├── haskell.svg
│   │   │   │   │   │   ├── haxe.svg
│   │   │   │   │   │   ├── hcl.svg
│   │   │   │   │   │   ├── hcl_light.svg
│   │   │   │   │   │   ├── helm.svg
│   │   │   │   │   │   ├── heroku.svg
│   │   │   │   │   │   ├── hex.svg
│   │   │   │   │   │   ├── histoire.svg
│   │   │   │   │   │   ├── hjson.svg
│   │   │   │   │   │   ├── horusec.svg
│   │   │   │   │   │   ├── hosts.svg
│   │   │   │   │   │   ├── hosts_light.svg
│   │   │   │   │   │   ├── hpp.svg
│   │   │   │   │   │   ├── html.svg
│   │   │   │   │   │   ├── http.svg
│   │   │   │   │   │   ├── huff.svg
│   │   │   │   │   │   ├── huff_light.svg
│   │   │   │   │   │   ├── hurl.svg
│   │   │   │   │   │   ├── husky.svg
│   │   │   │   │   │   ├── i18n.svg
│   │   │   │   │   │   ├── idris.svg
│   │   │   │   │   │   ├── ifanr-cloud.svg
│   │   │   │   │   │   ├── image.svg
│   │   │   │   │   │   ├── imba.svg
│   │   │   │   │   │   ├── installation.svg
│   │   │   │   │   │   ├── ionic.svg
│   │   │   │   │   │   ├── istanbul.svg
│   │   │   │   │   │   ├── jar.svg
│   │   │   │   │   │   ├── java.svg
│   │   │   │   │   │   ├── javaclass.svg
│   │   │   │   │   │   ├── javascript-map.svg
│   │   │   │   │   │   ├── javascript.svg
│   │   │   │   │   │   ├── jenkins.svg
│   │   │   │   │   │   ├── jest.svg
│   │   │   │   │   │   ├── jinja.svg
│   │   │   │   │   │   ├── jinja_light.svg
│   │   │   │   │   │   ├── jsconfig.svg
│   │   │   │   │   │   ├── json.svg
│   │   │   │   │   │   ├── jsr.svg
│   │   │   │   │   │   ├── jsr_light.svg
│   │   │   │   │   │   ├── julia.svg
│   │   │   │   │   │   ├── jupyter.svg
│   │   │   │   │   │   ├── just.svg
│   │   │   │   │   │   ├── karma.svg
│   │   │   │   │   │   ├── kcl.svg
│   │   │   │   │   │   ├── key.svg
│   │   │   │   │   │   ├── keystatic.svg
│   │   │   │   │   │   ├── kivy.svg
│   │   │   │   │   │   ├── kl.svg
│   │   │   │   │   │   ├── knip.svg
│   │   │   │   │   │   ├── kotlin.svg
│   │   │   │   │   │   ├── kubernetes.svg
│   │   │   │   │   │   ├── kusto.svg
│   │   │   │   │   │   ├── label.svg
│   │   │   │   │   │   ├── laravel.svg
│   │   │   │   │   │   ├── latexmk.svg
│   │   │   │   │   │   ├── lbx.svg
│   │   │   │   │   │   ├── lefthook.svg
│   │   │   │   │   │   ├── lerna.svg
│   │   │   │   │   │   ├── less.svg
│   │   │   │   │   │   ├── liara.svg
│   │   │   │   │   │   ├── lib.svg
│   │   │   │   │   │   ├── lighthouse.svg
│   │   │   │   │   │   ├── lilypond.svg
│   │   │   │   │   │   ├── lintstaged.svg
│   │   │   │   │   │   ├── liquid.svg
│   │   │   │   │   │   ├── lisp.svg
│   │   │   │   │   │   ├── livescript.svg
│   │   │   │   │   │   ├── lock.svg
│   │   │   │   │   │   ├── log.svg
│   │   │   │   │   │   ├── lolcode.svg
│   │   │   │   │   │   ├── lottie.svg
│   │   │   │   │   │   ├── lua.svg
│   │   │   │   │   │   ├── luau.svg
│   │   │   │   │   │   ├── lyric.svg
│   │   │   │   │   │   ├── makefile.svg
│   │   │   │   │   │   ├── markdoc-config.svg
│   │   │   │   │   │   ├── markdoc.svg
│   │   │   │   │   │   ├── markdown.svg
│   │   │   │   │   │   ├── markdownlint.svg
│   │   │   │   │   │   ├── markojs.svg
│   │   │   │   │   │   ├── mathematica.svg
│   │   │   │   │   │   ├── matlab.svg
│   │   │   │   │   │   ├── maven.svg
│   │   │   │   │   │   ├── mdsvex.svg
│   │   │   │   │   │   ├── mdx.svg
│   │   │   │   │   │   ├── mercurial.svg
│   │   │   │   │   │   ├── merlin.svg
│   │   │   │   │   │   ├── mermaid.svg
│   │   │   │   │   │   ├── meson.svg
│   │   │   │   │   │   ├── minecraft-fabric.svg
│   │   │   │   │   │   ├── minecraft.svg
│   │   │   │   │   │   ├── mint.svg
│   │   │   │   │   │   ├── mjml.svg
│   │   │   │   │   │   ├── mocha.svg
│   │   │   │   │   │   ├── modernizr.svg
│   │   │   │   │   │   ├── mojo.svg
│   │   │   │   │   │   ├── moon.svg
│   │   │   │   │   │   ├── moonscript.svg
│   │   │   │   │   │   ├── mxml.svg
│   │   │   │   │   │   ├── nano-staged.svg
│   │   │   │   │   │   ├── nano-staged_light.svg
│   │   │   │   │   │   ├── ndst.svg
│   │   │   │   │   │   ├── nest.svg
│   │   │   │   │   │   ├── netlify.svg
│   │   │   │   │   │   ├── netlify_light.svg
│   │   │   │   │   │   ├── next.svg
│   │   │   │   │   │   ├── next_light.svg
│   │   │   │   │   │   ├── nginx.svg
│   │   │   │   │   │   ├── ngrx-actions.svg
│   │   │   │   │   │   ├── ngrx-effects.svg
│   │   │   │   │   │   ├── ngrx-entity.svg
│   │   │   │   │   │   ├── ngrx-reducer.svg
│   │   │   │   │   │   ├── ngrx-selectors.svg
│   │   │   │   │   │   ├── ngrx-state.svg
│   │   │   │   │   │   ├── nim.svg
│   │   │   │   │   │   ├── nix.svg
│   │   │   │   │   │   ├── nodejs.svg
│   │   │   │   │   │   ├── nodejs_alt.svg
│   │   │   │   │   │   ├── nodemon.svg
│   │   │   │   │   │   ├── npm.svg
│   │   │   │   │   │   ├── nuget.svg
│   │   │   │   │   │   ├── nunjucks.svg
│   │   │   │   │   │   ├── nuxt.svg
│   │   │   │   │   │   ├── nx.svg
│   │   │   │   │   │   ├── objective-c.svg
│   │   │   │   │   │   ├── objective-cpp.svg
│   │   │   │   │   │   ├── ocaml.svg
│   │   │   │   │   │   ├── odin.svg
│   │   │   │   │   │   ├── opa.svg
│   │   │   │   │   │   ├── opam.svg
│   │   │   │   │   │   ├── openapi.svg
│   │   │   │   │   │   ├── openapi_light.svg
│   │   │   │   │   │   ├── otne.svg
│   │   │   │   │   │   ├── oxlint.svg
│   │   │   │   │   │   ├── packship.svg
│   │   │   │   │   │   ├── palette.svg
│   │   │   │   │   │   ├── panda.svg
│   │   │   │   │   │   ├── parcel.svg
│   │   │   │   │   │   ├── pascal.svg
│   │   │   │   │   │   ├── pawn.svg
│   │   │   │   │   │   ├── payload.svg
│   │   │   │   │   │   ├── payload_light.svg
│   │   │   │   │   │   ├── pdf.svg
│   │   │   │   │   │   ├── pdm.svg
│   │   │   │   │   │   ├── percy.svg
│   │   │   │   │   │   ├── perl.svg
│   │   │   │   │   │   ├── php-cs-fixer.svg
│   │   │   │   │   │   ├── php.svg
│   │   │   │   │   │   ├── phpstan.svg
│   │   │   │   │   │   ├── phpunit.svg
│   │   │   │   │   │   ├── php_elephant.svg
│   │   │   │   │   │   ├── php_elephant_pink.svg
│   │   │   │   │   │   ├── pinejs.svg
│   │   │   │   │   │   ├── pipeline.svg
│   │   │   │   │   │   ├── pkl.svg
│   │   │   │   │   │   ├── plastic.svg
│   │   │   │   │   │   ├── playwright.svg
│   │   │   │   │   │   ├── plop.svg
│   │   │   │   │   │   ├── pm2-ecosystem.svg
│   │   │   │   │   │   ├── pnpm.svg
│   │   │   │   │   │   ├── pnpm_light.svg
│   │   │   │   │   │   ├── poetry.svg
│   │   │   │   │   │   ├── postcss.svg
│   │   │   │   │   │   ├── posthtml.svg
│   │   │   │   │   │   ├── powerpoint.svg
│   │   │   │   │   │   ├── powershell.svg
│   │   │   │   │   │   ├── pre-commit.svg
│   │   │   │   │   │   ├── prettier.svg
│   │   │   │   │   │   ├── prisma.svg
│   │   │   │   │   │   ├── processing.svg
│   │   │   │   │   │   ├── prolog.svg
│   │   │   │   │   │   ├── prompt.svg
│   │   │   │   │   │   ├── proto.svg
│   │   │   │   │   │   ├── protractor.svg
│   │   │   │   │   │   ├── pug.svg
│   │   │   │   │   │   ├── puppet.svg
│   │   │   │   │   │   ├── puppeteer.svg
│   │   │   │   │   │   ├── purescript.svg
│   │   │   │   │   │   ├── python-misc.svg
│   │   │   │   │   │   ├── python.svg
│   │   │   │   │   │   ├── pytorch.svg
│   │   │   │   │   │   ├── qsharp.svg
│   │   │   │   │   │   ├── quarto.svg
│   │   │   │   │   │   ├── quasar.svg
│   │   │   │   │   │   ├── quokka.svg
│   │   │   │   │   │   ├── qwik.svg
│   │   │   │   │   │   ├── r.svg
│   │   │   │   │   │   ├── racket.svg
│   │   │   │   │   │   ├── raml.svg
│   │   │   │   │   │   ├── razor.svg
│   │   │   │   │   │   ├── rbxmk.svg
│   │   │   │   │   │   ├── rc.svg
│   │   │   │   │   │   ├── react.svg
│   │   │   │   │   │   ├── react_ts.svg
│   │   │   │   │   │   ├── readme.svg
│   │   │   │   │   │   ├── reason.svg
│   │   │   │   │   │   ├── red.svg
│   │   │   │   │   │   ├── redux-action.svg
│   │   │   │   │   │   ├── redux-reducer.svg
│   │   │   │   │   │   ├── redux-selector.svg
│   │   │   │   │   │   ├── redux-store.svg
│   │   │   │   │   │   ├── regedit.svg
│   │   │   │   │   │   ├── remark.svg
│   │   │   │   │   │   ├── remix.svg
│   │   │   │   │   │   ├── remix_light.svg
│   │   │   │   │   │   ├── renovate.svg
│   │   │   │   │   │   ├── replit.svg
│   │   │   │   │   │   ├── rescript-interface.svg
│   │   │   │   │   │   ├── rescript.svg
│   │   │   │   │   │   ├── restql.svg
│   │   │   │   │   │   ├── riot.svg
│   │   │   │   │   │   ├── roadmap.svg
│   │   │   │   │   │   ├── roblox.svg
│   │   │   │   │   │   ├── robot.svg
│   │   │   │   │   │   ├── robots.svg
│   │   │   │   │   │   ├── rocket.svg
│   │   │   │   │   │   ├── rojo.svg
│   │   │   │   │   │   ├── rollup.svg
│   │   │   │   │   │   ├── rome.svg
│   │   │   │   │   │   ├── routing.svg
│   │   │   │   │   │   ├── rspec.svg
│   │   │   │   │   │   ├── rubocop.svg
│   │   │   │   │   │   ├── rubocop_light.svg
│   │   │   │   │   │   ├── ruby.svg
│   │   │   │   │   │   ├── ruff.svg
│   │   │   │   │   │   ├── rust.svg
│   │   │   │   │   │   ├── salesforce.svg
│   │   │   │   │   │   ├── san.svg
│   │   │   │   │   │   ├── sas.svg
│   │   │   │   │   │   ├── sass.svg
│   │   │   │   │   │   ├── sbt.svg
│   │   │   │   │   │   ├── scala.svg
│   │   │   │   │   │   ├── scheme.svg
│   │   │   │   │   │   ├── scons.svg
│   │   │   │   │   │   ├── scons_light.svg
│   │   │   │   │   │   ├── screwdriver.svg
│   │   │   │   │   │   ├── search.svg
│   │   │   │   │   │   ├── semantic-release.svg
│   │   │   │   │   │   ├── semantic-release_light.svg
│   │   │   │   │   │   ├── semgrep.svg
│   │   │   │   │   │   ├── sentry.svg
│   │   │   │   │   │   ├── sequelize.svg
│   │   │   │   │   │   ├── serverless.svg
│   │   │   │   │   │   ├── settings.svg
│   │   │   │   │   │   ├── shader.svg
│   │   │   │   │   │   ├── silverstripe.svg
│   │   │   │   │   │   ├── simulink.svg
│   │   │   │   │   │   ├── siyuan.svg
│   │   │   │   │   │   ├── sketch.svg
│   │   │   │   │   │   ├── slim.svg
│   │   │   │   │   │   ├── slint.svg
│   │   │   │   │   │   ├── slug.svg
│   │   │   │   │   │   ├── smarty.svg
│   │   │   │   │   │   ├── sml.svg
│   │   │   │   │   │   ├── snakemake.svg
│   │   │   │   │   │   ├── snapcraft.svg
│   │   │   │   │   │   ├── snowpack.svg
│   │   │   │   │   │   ├── snowpack_light.svg
│   │   │   │   │   │   ├── snyk.svg
│   │   │   │   │   │   ├── solidity.svg
│   │   │   │   │   │   ├── sonarcloud.svg
│   │   │   │   │   │   ├── spwn.svg
│   │   │   │   │   │   ├── stackblitz.svg
│   │   │   │   │   │   ├── stan.svg
│   │   │   │   │   │   ├── steadybit.svg
│   │   │   │   │   │   ├── stencil.svg
│   │   │   │   │   │   ├── stitches.svg
│   │   │   │   │   │   ├── stitches_light.svg
│   │   │   │   │   │   ├── storybook.svg
│   │   │   │   │   │   ├── stryker.svg
│   │   │   │   │   │   ├── stylable.svg
│   │   │   │   │   │   ├── stylelint.svg
│   │   │   │   │   │   ├── stylelint_light.svg
│   │   │   │   │   │   ├── stylus.svg
│   │   │   │   │   │   ├── sublime.svg
│   │   │   │   │   │   ├── subtitles.svg
│   │   │   │   │   │   ├── supabase.svg
│   │   │   │   │   │   ├── svelte.svg
│   │   │   │   │   │   ├── svg.svg
│   │   │   │   │   │   ├── svgo.svg
│   │   │   │   │   │   ├── svgr.svg
│   │   │   │   │   │   ├── swagger.svg
│   │   │   │   │   │   ├── sway.svg
│   │   │   │   │   │   ├── swc.svg
│   │   │   │   │   │   ├── swift.svg
│   │   │   │   │   │   ├── syncpack.svg
│   │   │   │   │   │   ├── systemd.svg
│   │   │   │   │   │   ├── systemd_light.svg
│   │   │   │   │   │   ├── table.svg
│   │   │   │   │   │   ├── tailwindcss.svg
│   │   │   │   │   │   ├── taskfile.svg
│   │   │   │   │   │   ├── tauri.svg
│   │   │   │   │   │   ├── taze.svg
│   │   │   │   │   │   ├── tcl.svg
│   │   │   │   │   │   ├── teal.svg
│   │   │   │   │   │   ├── templ.svg
│   │   │   │   │   │   ├── template.svg
│   │   │   │   │   │   ├── terraform.svg
│   │   │   │   │   │   ├── test-js.svg
│   │   │   │   │   │   ├── test-jsx.svg
│   │   │   │   │   │   ├── test-ts.svg
│   │   │   │   │   │   ├── tex.svg
│   │   │   │   │   │   ├── textlint.svg
│   │   │   │   │   │   ├── tilt.svg
│   │   │   │   │   │   ├── tldraw.svg
│   │   │   │   │   │   ├── tldraw_light.svg
│   │   │   │   │   │   ├── tobi.svg
│   │   │   │   │   │   ├── tobimake.svg
│   │   │   │   │   │   ├── todo.svg
│   │   │   │   │   │   ├── toml.svg
│   │   │   │   │   │   ├── toml_light.svg
│   │   │   │   │   │   ├── travis.svg
│   │   │   │   │   │   ├── tree.svg
│   │   │   │   │   │   ├── trigger.svg
│   │   │   │   │   │   ├── tsconfig.svg
│   │   │   │   │   │   ├── tsdoc.svg
│   │   │   │   │   │   ├── tsil.svg
│   │   │   │   │   │   ├── tune.svg
│   │   │   │   │   │   ├── turborepo.svg
│   │   │   │   │   │   ├── turborepo_light.svg
│   │   │   │   │   │   ├── twig.svg
│   │   │   │   │   │   ├── twine.svg
│   │   │   │   │   │   ├── typescript-def.svg
│   │   │   │   │   │   ├── typescript.svg
│   │   │   │   │   │   ├── typst.svg
│   │   │   │   │   │   ├── umi.svg
│   │   │   │   │   │   ├── uml.svg
│   │   │   │   │   │   ├── uml_light.svg
│   │   │   │   │   │   ├── unity.svg
│   │   │   │   │   │   ├── unocss.svg
│   │   │   │   │   │   ├── url.svg
│   │   │   │   │   │   ├── uv.svg
│   │   │   │   │   │   ├── vagrant.svg
│   │   │   │   │   │   ├── vala.svg
│   │   │   │   │   │   ├── vanilla-extract.svg
│   │   │   │   │   │   ├── varnish.svg
│   │   │   │   │   │   ├── vedic.svg
│   │   │   │   │   │   ├── velite.svg
│   │   │   │   │   │   ├── velocity.svg
│   │   │   │   │   │   ├── vercel.svg
│   │   │   │   │   │   ├── vercel_light.svg
│   │   │   │   │   │   ├── verdaccio.svg
│   │   │   │   │   │   ├── verified.svg
│   │   │   │   │   │   ├── verilog.svg
│   │   │   │   │   │   ├── vfl.svg
│   │   │   │   │   │   ├── video.svg
│   │   │   │   │   │   ├── vim.svg
│   │   │   │   │   │   ├── virtual.svg
│   │   │   │   │   │   ├── visualstudio.svg
│   │   │   │   │   │   ├── vite.svg
│   │   │   │   │   │   ├── vitest.svg
│   │   │   │   │   │   ├── vlang.svg
│   │   │   │   │   │   ├── vscode.svg
│   │   │   │   │   │   ├── vue-config.svg
│   │   │   │   │   │   ├── vue.svg
│   │   │   │   │   │   ├── vuex-store.svg
│   │   │   │   │   │   ├── wakatime.svg
│   │   │   │   │   │   ├── wakatime_light.svg
│   │   │   │   │   │   ├── wallaby.svg
│   │   │   │   │   │   ├── wally.svg
│   │   │   │   │   │   ├── watchman.svg
│   │   │   │   │   │   ├── webassembly.svg
│   │   │   │   │   │   ├── webhint.svg
│   │   │   │   │   │   ├── webpack.svg
│   │   │   │   │   │   ├── wepy.svg
│   │   │   │   │   │   ├── werf.svg
│   │   │   │   │   │   ├── windicss.svg
│   │   │   │   │   │   ├── wolframlanguage.svg
│   │   │   │   │   │   ├── word.svg
│   │   │   │   │   │   ├── wrangler.svg
│   │   │   │   │   │   ├── wxt.svg
│   │   │   │   │   │   ├── xaml.svg
│   │   │   │   │   │   ├── xmake.svg
│   │   │   │   │   │   ├── xml.svg
│   │   │   │   │   │   ├── yaml.svg
│   │   │   │   │   │   ├── yang.svg
│   │   │   │   │   │   ├── yarn.svg
│   │   │   │   │   │   ├── zeabur.svg
│   │   │   │   │   │   ├── zeabur_light.svg
│   │   │   │   │   │   ├── zig.svg
│   │   │   │   │   │   └── zip.svg
│   │   │   │   │   └── provider
│   │   │   │   │       ├── 302ai.svg
│   │   │   │   │       ├── abacus.svg
│   │   │   │   │       ├── aihubmix.svg
│   │   │   │   │       ├── alibaba-cn.svg
│   │   │   │   │       ├── alibaba-coding-plan-cn.svg
│   │   │   │   │       ├── alibaba-coding-plan.svg
│   │   │   │   │       ├── alibaba.svg
│   │   │   │   │       ├── amazon-bedrock.svg
│   │   │   │   │       ├── anthropic.svg
│   │   │   │   │       ├── azure-cognitive-services.svg
│   │   │   │   │       ├── azure.svg
│   │   │   │   │       ├── bailing.svg
│   │   │   │   │       ├── baseten.svg
│   │   │   │   │       ├── berget.svg
│   │   │   │   │       ├── cerebras.svg
│   │   │   │   │       ├── chutes.svg
│   │   │   │   │       ├── clarifai.svg
│   │   │   │   │       ├── cloudferro-sherlock.svg
│   │   │   │   │       ├── cloudflare-ai-gateway.svg
│   │   │   │   │       ├── cloudflare-workers-ai.svg
│   │   │   │   │       ├── cohere.svg
│   │   │   │   │       ├── cortecs.svg
│   │   │   │   │       ├── deepinfra.svg
│   │   │   │   │       ├── deepseek.svg
│   │   │   │   │       ├── dinference.svg
│   │   │   │   │       ├── drun.svg
│   │   │   │   │       ├── evroc.svg
│   │   │   │   │       ├── fastrouter.svg
│   │   │   │   │       ├── fireworks-ai.svg
│   │   │   │   │       ├── firmware.svg
│   │   │   │   │       ├── friendli.svg
│   │   │   │   │       ├── github-copilot.svg
│   │   │   │   │       ├── github-models.svg
│   │   │   │   │       ├── gitlab.svg
│   │   │   │   │       ├── google-vertex-anthropic.svg
│   │   │   │   │       ├── google-vertex.svg
│   │   │   │   │       ├── google.svg
│   │   │   │   │       ├── groq.svg
│   │   │   │   │       ├── helicone.svg
│   │   │   │   │       ├── huggingface.svg
│   │   │   │   │       ├── iflowcn.svg
│   │   │   │   │       ├── inception.svg
│   │   │   │   │       ├── inference.svg
│   │   │   │   │       ├── io-net.svg
│   │   │   │   │       ├── jiekou.svg
│   │   │   │   │       ├── kilo.svg
│   │   │   │   │       ├── kimi-for-coding.svg
│   │   │   │   │       ├── kuae-cloud-coding-plan.svg
│   │   │   │   │       ├── llama.svg
│   │   │   │   │       ├── lmstudio.svg
│   │   │   │   │       ├── lucidquery.svg
│   │   │   │   │       ├── meganova.svg
│   │   │   │   │       ├── minimax-cn-coding-plan.svg
│   │   │   │   │       ├── minimax-cn.svg
│   │   │   │   │       ├── minimax-coding-plan.svg
│   │   │   │   │       ├── minimax.svg
│   │   │   │   │       ├── mistral.svg
│   │   │   │   │       ├── moark.svg
│   │   │   │   │       ├── modelscope.svg
│   │   │   │   │       ├── moonshotai-cn.svg
│   │   │   │   │       ├── moonshotai.svg
│   │   │   │   │       ├── morph.svg
│   │   │   │   │       ├── nano-gpt.svg
│   │   │   │   │       ├── nebius.svg
│   │   │   │   │       ├── nova.svg
│   │   │   │   │       ├── novita-ai.svg
│   │   │   │   │       ├── nvidia.svg
│   │   │   │   │       ├── ollama-cloud.svg
│   │   │   │   │       ├── openai.svg
│   │   │   │   │       ├── opencode-go.svg
│   │   │   │   │       ├── opencode.svg
│   │   │   │   │       ├── openrouter.svg
│   │   │   │   │       ├── ovhcloud.svg
│   │   │   │   │       ├── perplexity-agent.svg
│   │   │   │   │       ├── perplexity.svg
│   │   │   │   │       ├── poe.svg
│   │   │   │   │       ├── privatemode-ai.svg
│   │   │   │   │       ├── qihang-ai.svg
│   │   │   │   │       ├── qiniu-ai.svg
│   │   │   │   │       ├── requesty.svg
│   │   │   │   │       ├── sap-ai-core.svg
│   │   │   │   │       ├── scaleway.svg
│   │   │   │   │       ├── siliconflow-cn.svg
│   │   │   │   │       ├── siliconflow.svg
│   │   │   │   │       ├── stackit.svg
│   │   │   │   │       ├── stepfun.svg
│   │   │   │   │       ├── submodel.svg
│   │   │   │   │       ├── synthetic.svg
│   │   │   │   │       ├── tencent-coding-plan.svg
│   │   │   │   │       ├── togetherai.svg
│   │   │   │   │       ├── upstage.svg
│   │   │   │   │       ├── v0.svg
│   │   │   │   │       ├── venice.svg
│   │   │   │   │       ├── vercel.svg
│   │   │   │   │       ├── vivgrid.svg
│   │   │   │   │       ├── vultr.svg
│   │   │   │   │       ├── wandb.svg
│   │   │   │   │       ├── xai.svg
│   │   │   │   │       ├── xiaomi.svg
│   │   │   │   │       ├── zai-coding-plan.svg
│   │   │   │   │       ├── zai.svg
│   │   │   │   │       ├── zenmux.svg
│   │   │   │   │       ├── zhipuai-coding-plan.svg
│   │   │   │   │       └── zhipuai.svg
│   │   │   │   └── images
│   │   │   │       ├── social-share-black.png
│   │   │   │       ├── social-share-zen.png
│   │   │   │       └── social-share.png
│   │   │   ├── components
│   │   │   │   ├── accordion.css
│   │   │   │   ├── accordion.stories.tsx
│   │   │   │   ├── accordion.tsx
│   │   │   │   ├── animated-number.css
│   │   │   │   ├── animated-number.tsx
│   │   │   │   ├── app-icon.css
│   │   │   │   ├── app-icon.stories.tsx
│   │   │   │   ├── app-icon.tsx
│   │   │   │   ├── app-icons
│   │   │   │   │   ├── sprite.svg
│   │   │   │   │   └── types.ts
│   │   │   │   ├── apply-patch-file.test.ts
│   │   │   │   ├── apply-patch-file.ts
│   │   │   │   ├── avatar.css
│   │   │   │   ├── avatar.stories.tsx
│   │   │   │   ├── avatar.tsx
│   │   │   │   ├── basic-tool.css
│   │   │   │   ├── basic-tool.stories.tsx
│   │   │   │   ├── basic-tool.tsx
│   │   │   │   ├── button.css
│   │   │   │   ├── button.stories.tsx
│   │   │   │   ├── button.tsx
│   │   │   │   ├── card.css
│   │   │   │   ├── card.stories.tsx
│   │   │   │   ├── card.tsx
│   │   │   │   ├── checkbox.css
│   │   │   │   ├── checkbox.stories.tsx
│   │   │   │   ├── checkbox.tsx
│   │   │   │   ├── collapsible.css
│   │   │   │   ├── collapsible.stories.tsx
│   │   │   │   ├── collapsible.tsx
│   │   │   │   ├── context-menu.css
│   │   │   │   ├── context-menu.stories.tsx
│   │   │   │   ├── context-menu.tsx
│   │   │   │   ├── dialog.css
│   │   │   │   ├── dialog.stories.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── diff-changes.css
│   │   │   │   ├── diff-changes.stories.tsx
│   │   │   │   ├── diff-changes.tsx
│   │   │   │   ├── dock-prompt.stories.tsx
│   │   │   │   ├── dock-prompt.tsx
│   │   │   │   ├── dock-surface.css
│   │   │   │   ├── dock-surface.tsx
│   │   │   │   ├── dropdown-menu.css
│   │   │   │   ├── dropdown-menu.stories.tsx
│   │   │   │   ├── dropdown-menu.tsx
│   │   │   │   ├── favicon.stories.tsx
│   │   │   │   ├── favicon.tsx
│   │   │   │   ├── file-icon.css
│   │   │   │   ├── file-icon.stories.tsx
│   │   │   │   ├── file-icon.tsx
│   │   │   │   ├── file-icons
│   │   │   │   │   ├── sprite.svg
│   │   │   │   │   └── types.ts
│   │   │   │   ├── file-media.tsx
│   │   │   │   ├── file-search.tsx
│   │   │   │   ├── file-ssr.tsx
│   │   │   │   ├── file.css
│   │   │   │   ├── file.tsx
│   │   │   │   ├── font.stories.tsx
│   │   │   │   ├── font.tsx
│   │   │   │   ├── hover-card.css
│   │   │   │   ├── hover-card.stories.tsx
│   │   │   │   ├── hover-card.tsx
│   │   │   │   ├── icon-button.css
│   │   │   │   ├── icon-button.stories.tsx
│   │   │   │   ├── icon-button.tsx
│   │   │   │   ├── icon.css
│   │   │   │   ├── icon.stories.tsx
│   │   │   │   ├── icon.tsx
│   │   │   │   ├── image-preview.css
│   │   │   │   ├── image-preview.stories.tsx
│   │   │   │   ├── image-preview.tsx
│   │   │   │   ├── inline-input.css
│   │   │   │   ├── inline-input.stories.tsx
│   │   │   │   ├── inline-input.tsx
│   │   │   │   ├── keybind.css
│   │   │   │   ├── keybind.stories.tsx
│   │   │   │   ├── keybind.tsx
│   │   │   │   ├── line-comment-annotations.tsx
│   │   │   │   ├── line-comment-styles.ts
│   │   │   │   ├── line-comment.stories.tsx
│   │   │   │   ├── line-comment.tsx
│   │   │   │   ├── list.css
│   │   │   │   ├── list.stories.tsx
│   │   │   │   ├── list.tsx
│   │   │   │   ├── logo.css
│   │   │   │   ├── logo.stories.tsx
│   │   │   │   ├── logo.tsx
│   │   │   │   ├── markdown-stream.test.ts
│   │   │   │   ├── markdown-stream.ts
│   │   │   │   ├── markdown.css
│   │   │   │   ├── markdown.stories.tsx
│   │   │   │   ├── markdown.tsx
│   │   │   │   ├── message-file.test.ts
│   │   │   │   ├── message-file.ts
│   │   │   │   ├── message-nav.css
│   │   │   │   ├── message-nav.stories.tsx
│   │   │   │   ├── message-nav.tsx
│   │   │   │   ├── message-part.css
│   │   │   │   ├── message-part.stories.tsx
│   │   │   │   ├── message-part.tsx
│   │   │   │   ├── motion-spring.tsx
│   │   │   │   ├── popover.css
│   │   │   │   ├── popover.stories.tsx
│   │   │   │   ├── popover.tsx
│   │   │   │   ├── progress-circle.css
│   │   │   │   ├── progress-circle.stories.tsx
│   │   │   │   ├── progress-circle.tsx
│   │   │   │   ├── progress.css
│   │   │   │   ├── progress.stories.tsx
│   │   │   │   ├── progress.tsx
│   │   │   │   ├── provider-icon.css
│   │   │   │   ├── provider-icon.stories.tsx
│   │   │   │   ├── provider-icon.tsx
│   │   │   │   ├── provider-icons
│   │   │   │   │   ├── sprite.svg
│   │   │   │   │   └── types.ts
│   │   │   │   ├── radio-group.css
│   │   │   │   ├── radio-group.stories.tsx
│   │   │   │   ├── radio-group.tsx
│   │   │   │   ├── resize-handle.css
│   │   │   │   ├── resize-handle.stories.tsx
│   │   │   │   ├── resize-handle.tsx
│   │   │   │   ├── scroll-view.css
│   │   │   │   ├── scroll-view.test.ts
│   │   │   │   ├── scroll-view.tsx
│   │   │   │   ├── select.css
│   │   │   │   ├── select.stories.tsx
│   │   │   │   ├── select.tsx
│   │   │   │   ├── session-diff.test.ts
│   │   │   │   ├── session-diff.ts
│   │   │   │   ├── session-retry.tsx
│   │   │   │   ├── session-review.css
│   │   │   │   ├── session-review.stories.tsx
│   │   │   │   ├── session-review.tsx
│   │   │   │   ├── session-turn.css
│   │   │   │   ├── session-turn.stories.tsx
│   │   │   │   ├── session-turn.tsx
│   │   │   │   ├── shell-submessage-motion.stories.tsx
│   │   │   │   ├── shell-submessage.css
│   │   │   │   ├── spinner.css
│   │   │   │   ├── spinner.stories.tsx
│   │   │   │   ├── spinner.tsx
│   │   │   │   ├── sticky-accordion-header.css
│   │   │   │   ├── sticky-accordion-header.stories.tsx
│   │   │   │   ├── sticky-accordion-header.tsx
│   │   │   │   ├── switch.css
│   │   │   │   ├── switch.stories.tsx
│   │   │   │   ├── switch.tsx
│   │   │   │   ├── tabs.css
│   │   │   │   ├── tabs.stories.tsx
│   │   │   │   ├── tabs.tsx
│   │   │   │   ├── tag.css
│   │   │   │   ├── tag.stories.tsx
│   │   │   │   ├── tag.tsx
│   │   │   │   ├── text-field.css
│   │   │   │   ├── text-field.stories.tsx
│   │   │   │   ├── text-field.tsx
│   │   │   │   ├── text-reveal.css
│   │   │   │   ├── text-reveal.stories.tsx
│   │   │   │   ├── text-reveal.tsx
│   │   │   │   ├── text-shimmer.css
│   │   │   │   ├── text-shimmer.stories.tsx
│   │   │   │   ├── text-shimmer.tsx
│   │   │   │   ├── text-strikethrough.css
│   │   │   │   ├── text-strikethrough.stories.tsx
│   │   │   │   ├── text-strikethrough.tsx
│   │   │   │   ├── thinking-heading.stories.tsx
│   │   │   │   ├── timeline-playground.stories.tsx
│   │   │   │   ├── toast.css
│   │   │   │   ├── toast.stories.tsx
│   │   │   │   ├── toast.tsx
│   │   │   │   ├── todo-panel-motion.stories.tsx
│   │   │   │   ├── tool-count-label.css
│   │   │   │   ├── tool-count-label.tsx
│   │   │   │   ├── tool-count-summary.css
│   │   │   │   ├── tool-count-summary.stories.tsx
│   │   │   │   ├── tool-count-summary.tsx
│   │   │   │   ├── tool-error-card.css
│   │   │   │   ├── tool-error-card.stories.tsx
│   │   │   │   ├── tool-error-card.tsx
│   │   │   │   ├── tool-status-title.css
│   │   │   │   ├── tool-status-title.tsx
│   │   │   │   ├── tooltip.css
│   │   │   │   ├── tooltip.stories.tsx
│   │   │   │   ├── tooltip.tsx
│   │   │   │   ├── typewriter.css
│   │   │   │   ├── typewriter.stories.tsx
│   │   │   │   └── typewriter.tsx
│   │   │   ├── context
│   │   │   │   ├── data.tsx
│   │   │   │   ├── dialog.tsx
│   │   │   │   ├── file.tsx
│   │   │   │   ├── helper.tsx
│   │   │   │   ├── i18n.tsx
│   │   │   │   ├── index.ts
│   │   │   │   ├── marked.tsx
│   │   │   │   └── worker-pool.tsx
│   │   │   ├── custom-elements.d.ts
│   │   │   ├── hooks
│   │   │   │   ├── create-auto-scroll.tsx
│   │   │   │   ├── index.ts
│   │   │   │   └── use-filtered-list.tsx
│   │   │   ├── i18n
│   │   │   │   ├── ar.ts
│   │   │   │   ├── br.ts
│   │   │   │   ├── bs.ts
│   │   │   │   ├── da.ts
│   │   │   │   ├── de.ts
│   │   │   │   ├── en.ts
│   │   │   │   ├── es.ts
│   │   │   │   ├── fr.ts
│   │   │   │   ├── ja.ts
│   │   │   │   ├── ko.ts
│   │   │   │   ├── no.ts
│   │   │   │   ├── pl.ts
│   │   │   │   ├── ru.ts
│   │   │   │   ├── th.ts
│   │   │   │   ├── tr.ts
│   │   │   │   ├── zh.ts
│   │   │   │   └── zht.ts
│   │   │   ├── pierre
│   │   │   │   ├── comment-hover.ts
│   │   │   │   ├── commented-lines.ts
│   │   │   │   ├── diff-selection.ts
│   │   │   │   ├── file-find.ts
│   │   │   │   ├── file-runtime.ts
│   │   │   │   ├── file-selection.ts
│   │   │   │   ├── index.ts
│   │   │   │   ├── media.ts
│   │   │   │   ├── selection-bridge.ts
│   │   │   │   ├── virtualizer.ts
│   │   │   │   └── worker.ts
│   │   │   ├── storybook
│   │   │   │   ├── fixtures.ts
│   │   │   │   └── scaffold.tsx
│   │   │   ├── styles
│   │   │   │   ├── animations.css
│   │   │   │   ├── base.css
│   │   │   │   ├── colors.css
│   │   │   │   ├── index.css
│   │   │   │   ├── tailwind
│   │   │   │   │   ├── colors.css
│   │   │   │   │   ├── index.css
│   │   │   │   │   └── utilities.css
│   │   │   │   ├── theme.css
│   │   │   │   └── utilities.css
│   │   │   └── theme
│   │   │       ├── color.ts
│   │   │       ├── context.tsx
│   │   │       ├── default-themes.ts
│   │   │       ├── desktop-theme.schema.json
│   │   │       ├── index.ts
│   │   │       ├── loader.ts
│   │   │       ├── resolve.ts
│   │   │       ├── themes
│   │   │       │   ├── amoled.json
│   │   │       │   ├── aura.json
│   │   │       │   ├── ayu.json
│   │   │       │   ├── carbonfox.json
│   │   │       │   ├── catppuccin-frappe.json
│   │   │       │   ├── catppuccin-macchiato.json
│   │   │       │   ├── catppuccin.json
│   │   │       │   ├── cobalt2.json
│   │   │       │   ├── cursor.json
│   │   │       │   ├── dracula.json
│   │   │       │   ├── everforest.json
│   │   │       │   ├── flexoki.json
│   │   │       │   ├── github.json
│   │   │       │   ├── gruvbox.json
│   │   │       │   ├── kanagawa.json
│   │   │       │   ├── lucent-orng.json
│   │   │       │   ├── material.json
│   │   │       │   ├── matrix.json
│   │   │       │   ├── mercury.json
│   │   │       │   ├── monokai.json
│   │   │       │   ├── nightowl.json
│   │   │       │   ├── nord.json
│   │   │       │   ├── oc-2.json
│   │   │       │   ├── one-dark.json
│   │   │       │   ├── onedarkpro.json
│   │   │       │   ├── opencode.json
│   │   │       │   ├── orng.json
│   │   │       │   ├── osaka-jade.json
│   │   │       │   ├── palenight.json
│   │   │       │   ├── rosepine.json
│   │   │       │   ├── shadesofpurple.json
│   │   │       │   ├── solarized.json
│   │   │       │   ├── synthwave84.json
│   │   │       │   ├── tokyonight.json
│   │   │       │   ├── vercel.json
│   │   │       │   ├── vesper.json
│   │   │       │   └── zenburn.json
│   │   │       └── types.ts
│   │   ├── sst-env.d.ts
│   │   ├── tsconfig.json
│   │   └── vite.config.ts
│   ├── ultron-mapper
│   │   ├── .opencode
│   │   │   └── map
│   │   │       ├── AI_INSTRUCTIONS.md
│   │   │       ├── ENTRY_POINTS.md
│   │   │       ├── STRUCTURE.md
│   │   │       └── TECH_STACK.md
│   │   ├── package.json
│   │   └── src
│   │       ├── AI_INSTRUCTIONS.md.template
│   │       ├── generator.ts
│   │       ├── index.ts
│   │       └── scanner.ts
│   └── web
│       ├── .gitignore
│       ├── astro.config.mjs
│       ├── config.mjs
│       ├── package.json
│       ├── public
│       │   ├── apple-touch-icon-v3.png
│       │   ├── apple-touch-icon.png
│       │   ├── favicon-96x96-v3.png
│       │   ├── favicon-96x96.png
│       │   ├── favicon-v3.ico
│       │   ├── favicon-v3.svg
│       │   ├── favicon.ico
│       │   ├── favicon.svg
│       │   ├── robots.txt
│       │   ├── site.webmanifest
│       │   ├── social-share-zen.png
│       │   ├── social-share.png
│       │   ├── theme.json
│       │   ├── web-app-manifest-192x192.png
│       │   └── web-app-manifest-512x512.png
│       ├── README.md
│       ├── src
│       │   ├── assets
│       │   │   ├── lander
│       │   │   │   ├── check.svg
│       │   │   │   ├── copy.svg
│       │   │   │   ├── screenshot-github.png
│       │   │   │   ├── screenshot-splash.png
│       │   │   │   ├── screenshot-vscode.png
│       │   │   │   └── screenshot.png
│       │   │   ├── logo-dark.svg
│       │   │   ├── logo-light.svg
│       │   │   ├── logo-ornate-dark.svg
│       │   │   ├── logo-ornate-light.svg
│       │   │   └── web
│       │   │       ├── web-homepage-active-session.png
│       │   │       ├── web-homepage-new-session.png
│       │   │       └── web-homepage-see-servers.png
│       │   ├── components
│       │   │   ├── Footer.astro
│       │   │   ├── Head.astro
│       │   │   ├── Header.astro
│       │   │   ├── Hero.astro
│       │   │   ├── icons
│       │   │   │   ├── custom.tsx
│       │   │   │   └── index.tsx
│       │   │   ├── Lander.astro
│       │   │   ├── share
│       │   │   │   ├── common.tsx
│       │   │   │   ├── content-bash.module.css
│       │   │   │   ├── content-bash.tsx
│       │   │   │   ├── content-code.module.css
│       │   │   │   ├── content-code.tsx
│       │   │   │   ├── content-diff.module.css
│       │   │   │   ├── content-diff.tsx
│       │   │   │   ├── content-error.module.css
│       │   │   │   ├── content-error.tsx
│       │   │   │   ├── content-markdown.module.css
│       │   │   │   ├── content-markdown.tsx
│       │   │   │   ├── content-text.module.css
│       │   │   │   ├── content-text.tsx
│       │   │   │   ├── copy-button.module.css
│       │   │   │   ├── copy-button.tsx
│       │   │   │   ├── part.module.css
│       │   │   │   └── part.tsx
│       │   │   ├── share.module.css
│       │   │   ├── Share.tsx
│       │   │   └── SiteTitle.astro
│       │   ├── content
│       │   │   ├── docs
│       │   │   │   ├── acp.mdx
│       │   │   │   ├── agents.mdx
│       │   │   │   ├── ar
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── bs
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── cli.mdx
│       │   │   │   ├── commands.mdx
│       │   │   │   ├── config.mdx
│       │   │   │   ├── custom-tools.mdx
│       │   │   │   ├── da
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── de
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── ecosystem.mdx
│       │   │   │   ├── enterprise.mdx
│       │   │   │   ├── es
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── formatters.mdx
│       │   │   │   ├── fr
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── github.mdx
│       │   │   │   ├── gitlab.mdx
│       │   │   │   ├── go.mdx
│       │   │   │   ├── ide.mdx
│       │   │   │   ├── index.mdx
│       │   │   │   ├── it
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── ja
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── keybinds.mdx
│       │   │   │   ├── ko
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── lsp.mdx
│       │   │   │   ├── mcp-servers.mdx
│       │   │   │   ├── models.mdx
│       │   │   │   ├── modes.mdx
│       │   │   │   ├── nb
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── network.mdx
│       │   │   │   ├── permissions.mdx
│       │   │   │   ├── pl
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── plugins.mdx
│       │   │   │   ├── providers.mdx
│       │   │   │   ├── pt-br
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── ru
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── rules.mdx
│       │   │   │   ├── sdk.mdx
│       │   │   │   ├── server.mdx
│       │   │   │   ├── share.mdx
│       │   │   │   ├── skills.mdx
│       │   │   │   ├── th
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── themes.mdx
│       │   │   │   ├── tools.mdx
│       │   │   │   ├── tr
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   ├── troubleshooting.mdx
│       │   │   │   ├── tui.mdx
│       │   │   │   ├── web.mdx
│       │   │   │   ├── windows-wsl.mdx
│       │   │   │   ├── zen.mdx
│       │   │   │   ├── zh-cn
│       │   │   │   │   ├── acp.mdx
│       │   │   │   │   ├── agents.mdx
│       │   │   │   │   ├── cli.mdx
│       │   │   │   │   ├── commands.mdx
│       │   │   │   │   ├── config.mdx
│       │   │   │   │   ├── custom-tools.mdx
│       │   │   │   │   ├── ecosystem.mdx
│       │   │   │   │   ├── enterprise.mdx
│       │   │   │   │   ├── formatters.mdx
│       │   │   │   │   ├── github.mdx
│       │   │   │   │   ├── gitlab.mdx
│       │   │   │   │   ├── go.mdx
│       │   │   │   │   ├── ide.mdx
│       │   │   │   │   ├── index.mdx
│       │   │   │   │   ├── keybinds.mdx
│       │   │   │   │   ├── lsp.mdx
│       │   │   │   │   ├── mcp-servers.mdx
│       │   │   │   │   ├── models.mdx
│       │   │   │   │   ├── modes.mdx
│       │   │   │   │   ├── network.mdx
│       │   │   │   │   ├── permissions.mdx
│       │   │   │   │   ├── plugins.mdx
│       │   │   │   │   ├── providers.mdx
│       │   │   │   │   ├── rules.mdx
│       │   │   │   │   ├── sdk.mdx
│       │   │   │   │   ├── server.mdx
│       │   │   │   │   ├── share.mdx
│       │   │   │   │   ├── skills.mdx
│       │   │   │   │   ├── themes.mdx
│       │   │   │   │   ├── tools.mdx
│       │   │   │   │   ├── troubleshooting.mdx
│       │   │   │   │   ├── tui.mdx
│       │   │   │   │   ├── web.mdx
│       │   │   │   │   ├── windows-wsl.mdx
│       │   │   │   │   └── zen.mdx
│       │   │   │   └── zh-tw
│       │   │   │       ├── acp.mdx
│       │   │   │       ├── agents.mdx
│       │   │   │       ├── cli.mdx
│       │   │   │       ├── commands.mdx
│       │   │   │       ├── config.mdx
│       │   │   │       ├── custom-tools.mdx
│       │   │   │       ├── ecosystem.mdx
│       │   │   │       ├── enterprise.mdx
│       │   │   │       ├── formatters.mdx
│       │   │   │       ├── github.mdx
│       │   │   │       ├── gitlab.mdx
│       │   │   │       ├── go.mdx
│       │   │   │       ├── ide.mdx
│       │   │   │       ├── index.mdx
│       │   │   │       ├── keybinds.mdx
│       │   │   │       ├── lsp.mdx
│       │   │   │       ├── mcp-servers.mdx
│       │   │   │       ├── models.mdx
│       │   │   │       ├── modes.mdx
│       │   │   │       ├── network.mdx
│       │   │   │       ├── permissions.mdx
│       │   │   │       ├── plugins.mdx
│       │   │   │       ├── providers.mdx
│       │   │   │       ├── rules.mdx
│       │   │   │       ├── sdk.mdx
│       │   │   │       ├── server.mdx
│       │   │   │       ├── share.mdx
│       │   │   │       ├── skills.mdx
│       │   │   │       ├── themes.mdx
│       │   │   │       ├── tools.mdx
│       │   │   │       ├── troubleshooting.mdx
│       │   │   │       ├── tui.mdx
│       │   │   │       ├── web.mdx
│       │   │   │       ├── windows-wsl.mdx
│       │   │   │       └── zen.mdx
│       │   │   └── i18n
│       │   │       ├── ar.json
│       │   │       ├── bs.json
│       │   │       ├── da.json
│       │   │       ├── de.json
│       │   │       ├── en.json
│       │   │       ├── es.json
│       │   │       ├── fr.json
│       │   │       ├── it.json
│       │   │       ├── ja.json
│       │   │       ├── ko.json
│       │   │       ├── nb.json
│       │   │       ├── pl.json
│       │   │       ├── pt-BR.json
│       │   │       ├── ru.json
│       │   │       ├── th.json
│       │   │       ├── tr.json
│       │   │       ├── zh-CN.json
│       │   │       └── zh-TW.json
│       │   ├── content.config.ts
│       │   ├── i18n
│       │   │   └── locales.ts
│       │   ├── middleware.ts
│       │   ├── pages
│       │   │   ├── s
│       │   │   │   └── [id].astro
│       │   │   └── [...slug].md.ts
│       │   ├── styles
│       │   │   └── custom.css
│       │   └── types
│       │       ├── lang-map.d.ts
│       │       └── starlight-virtual.d.ts
│       ├── sst-env.d.ts
│       └── tsconfig.json
├── README.ar.md
├── README.bn.md
├── README.br.md
├── README.bs.md
├── README.da.md
├── README.de.md
├── README.es.md
├── README.fr.md
├── README.gr.md
├── README.it.md
├── README.ja.md
├── README.ko.md
├── README.md
├── README.no.md
├── README.pl.md
├── README.ru.md
├── README.th.md
├── README.tr.md
├── README.uk.md
├── README.vi.md
├── README.zh.md
├── README.zht.md
├── script
│   ├── beta.ts
│   ├── changelog.ts
│   ├── duplicate-pr.ts
│   ├── format.ts
│   ├── generate.ts
│   ├── github
│   │   └── close-issues.ts
│   ├── hooks
│   ├── publish.ts
│   ├── raw-changelog.ts
│   ├── release
│   ├── roll-sessions.ts
│   ├── sign-windows.ps1
│   ├── stats.ts
│   ├── sync-zed.ts
│   └── version.ts
├── sdks
│   └── vscode
│       ├── .gitignore
│       ├── .vscode-test.mjs
│       ├── .vscodeignore
│       ├── bun.lock
│       ├── esbuild.js
│       ├── eslint.config.mjs
│       ├── images
│       │   ├── button-dark.svg
│       │   ├── button-light.svg
│       │   └── icon.png
│       ├── package.json
│       ├── README.md
│       ├── script
│       │   ├── publish
│       │   └── release
│       ├── src
│       │   └── extension.ts
│       ├── sst-env.d.ts
│       └── tsconfig.json
├── SECURITY.md
├── session.json
├── setup-ultron.ps1
├── setup-ultron.sh
├── specs
│   ├── project.md
│   └── v2
│       └── session.md
├── sst-env.d.ts
├── sst.config.ts
├── start-all.ps1
├── start.ts
├── STATS.md
├── swarm
│   ├── .env
│   ├── agents
│   │   ├── base_agent.py
│   │   ├── builder.py
│   │   ├── debugger.py
│   │   ├── designer.py
│   │   ├── planner.py
│   │   ├── verifier.py
│   │   └── __init__.py
│   ├── core
│   │   ├── agent_registry.py
│   │   ├── dag.py
│   │   ├── message_bus.py
│   │   ├── skill_orchestra.py
│   │   └── __init__.py
│   ├── evolution_agent.py
│   ├── llm_router.py
│   ├── locks
│   │   ├── design_ui_for
│   │   ├── run_a_simple_test
│   │   └── test_task
│   ├── logs
│   │   ├── builder.log
│   │   ├── debugger.log
│   │   ├── designer.log
│   │   ├── llm_calls.jsonl
│   │   ├── orchestrator.err.log
│   │   ├── orchestrator.log
│   │   ├── planner.log
│   │   └── verifier.log
│   ├── mcp_server.py
│   ├── memory
│   │   ├── chroma
│   │   │   ├── 1b0fd964-c8f2-4a9b-8bdb-dc22320f5749
│   │   │   │   ├── data_level0.bin
│   │   │   │   ├── header.bin
│   │   │   │   ├── length.bin
│   │   │   │   └── link_lists.bin
│   │   │   └── chroma.sqlite3
│   │   ├── planner
│   │   │   └── plan_282f39.json
│   │   └── shared
│   │       ├── state.sqlite
│   │       ├── state.sqlite-shm
│   │       └── state.sqlite-wal
│   ├── observability.py
│   ├── orchestrator.py
│   ├── projects
│   │   ├── project_584fbe
│   │   │   └── design
│   │   │       └── design_ui_for
│   │   ├── project_68b92b
│   │   │   ├── src
│   │   │   │   └── test_task
│   │   │   └── tests
│   │   │       └── test_test_task
│   │   └── project_b5b061
│   │       ├── src
│   │       │   └── run_a_simple_test
│   │       └── tests
│   │           └── test_run_a_simple_test
│   ├── proposals
│   │   ├── .gitkeep
│   │   ├── plan-optimize-v1.json
│   │   ├── plan_brevity_v1.json
│   │   └── plan_concise_v1.json
│   ├── rag
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── __init__.py
│   ├── README.md
│   ├── requirements.txt
│   ├── router_llm.py
│   ├── session_manager.py
│   ├── setup_db.py
│   ├── start.ps1
│   ├── swarm-tui.ps1
│   ├── swarm_config.py
│   ├── swarm_tui.py
│   ├── tasks
│   │   ├── processing
│   │   │   ├── .gitkeep
│   │   │   ├── task_05686281.json
│   │   │   ├── task_24e68b4b.json
│   │   │   ├── task_3621cf01.json
│   │   │   ├── task_449f6e98.json
│   │   │   ├── task_6e70660e.json
│   │   │   ├── task_81b050e8.json
│   │   │   └── task_e124d8ce.json
│   │   └── queue
│   │       └── .gitkeep
│   ├── test_all.py
│   ├── test_deepseek_direct.py
│   └── UPGRADE_LOG.md
├── SWARM_INTEGRATION.md
├── tsconfig.json
├── turbo.json
├── ultron-system
│   ├── core
│   │   ├── config.py
│   │   ├── file_tracker.py
│   │   ├── intelligence.py
│   │   ├── logger.py
│   │   ├── memory.py
│   │   ├── monitor.py
│   │   ├── optimizer.py
│   │   ├── privacy.py
│   │   ├── recovery.py
│   │   ├── startup.py
│   │   ├── state.py
│   │   └── tasks.py
│   ├── dashboard.py
│   ├── logs
│   │   ├── dashboard.log
│   │   ├── intelligence.log
│   │   ├── main.log
│   │   ├── memory.log
│   │   ├── monitor.log
│   │   ├── optimizer.log
│   │   ├── privacy.log
│   │   ├── recovery.log
│   │   ├── startup.log
│   │   └── tasks.log
│   ├── main.py
│   ├── memory
│   │   ├── .gitignore
│   │   ├── personal
│   │   │   └── profiles
│   │   │       └── moez.json
│   │   └── shared
│   │       ├── state.json
│   │       ├── tasks.db
│   │       ├── tasks.db-shm
│   │       └── tasks.db-wal
│   ├── requirements.txt
│   ├── start.ps1
│   └── ui
│       └── dashboard.html
├── ultron.txt
├── ultron_memory.json
└── verify-hands-eyes.ps1

```
