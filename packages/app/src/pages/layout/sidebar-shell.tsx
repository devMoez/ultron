import { createEffect, createSignal, For, Show, type Accessor, type JSX } from "solid-js"
import { type DragEvent } from "@thisbeyond/solid-dnd"
import { useLayout, type LocalProject } from "@/context/layout"
import { useNavigate, useParams } from "@solidjs/router"
import { type TabType, useSessionType } from "@/context/session-type"
import { usePinnedStore } from "@/context/pinned-store"
import { SwarmPanel } from "@/components/swarm-panel"

// ─── Tiny icon wrapper ───────────────────────────────────────────────────────
function Svg(props: { children: JSX.Element }) {
  return (
    <svg
      viewBox="0 0 24 24"
      width="16"
      height="16"
      fill="none"
      stroke="currentColor"
      stroke-width="1.8"
      stroke-linecap="round"
      stroke-linejoin="round"
    >
      {props.children}
    </svg>
  )
}

// ─── Icon set ────────────────────────────────────────────────────────────────
function IconSidebar() {
  return (
    <Svg>
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <line x1="9" y1="3" x2="9" y2="21" />
    </Svg>
  )
}
function IconSearch() {
  return (
    <Svg>
      <circle cx="11" cy="11" r="7" />
      <line x1="16.5" y1="16.5" x2="22" y2="22" />
    </Svg>
  )
}
function IconBack() {
  return (
    <Svg>
      <polyline points="15 18 9 12 15 6" />
    </Svg>
  )
}
function IconForward() {
  return (
    <Svg>
      <polyline points="9 18 15 12 9 6" />
    </Svg>
  )
}
function IconChat() {
  return (
    <Svg>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </Svg>
  )
}
function IconCode() {
  return (
    <Svg>
      <polyline points="16 18 22 12 16 6" />
      <polyline points="8 6 2 12 8 18" />
    </Svg>
  )
}
function IconCowork() {
  return (
    <Svg>
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </Svg>
  )
}
function IconPlus() {
  return (
    <Svg>
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </Svg>
  )
}
function IconFolder() {
  return (
    <Svg>
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </Svg>
  )
}
function IconStar() {
  return (
    <Svg>
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </Svg>
  )
}
function IconPen() {
  return (
    <Svg>
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
    </Svg>
  )
}
function IconUser() {
  return (
    <Svg>
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </Svg>
  )
}
function IconChevronRight() {
  return (
    <Svg>
      <polyline points="9 18 15 12 9 6" />
    </Svg>
  )
}
function IconLink() {
  return (
    <Svg>
      <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
      <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" />
    </Svg>
  )
}
function IconAgents() {
  return (
    <Svg>
      <circle cx="12" cy="8" r="3" />
      <path d="M6 20v-1a6 6 0 0 1 12 0v1" />
      <circle cx="20" cy="8" r="2" />
      <path d="M22 20v-1a4 4 0 0 0-4-4" />
      <circle cx="4" cy="8" r="2" />
      <path d="M2 20v-1a4 4 0 0 1 4-4" />
    </Svg>
  )
}

// ─── NavButton (top icon buttons) ────────────────────────────────────────────
function NavBtn(props: { title?: string; onClick?: () => void; children: JSX.Element }) {
  const [hov, setHov] = createSignal(false)
  return (
    <button
      title={props.title}
      onClick={props.onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        width: "32px",
        height: "32px",
        "border-radius": "7px",
        display: "flex",
        "align-items": "center",
        "justify-content": "center",
        color: hov() ? "#e8e8e8" : "#888",
        cursor: "pointer",
        background: hov() ? "#2a2a2a" : "transparent",
        border: "none",
        transition: "background .15s, color .15s",
        "flex-shrink": "0",
        padding: "0",
      }}
    >
      {props.children}
    </button>
  )
}

// ─── Tab button ──────────────────────────────────────────────────────────────
function TabBtn(props: { active: boolean; label: string; icon: JSX.Element; onClick: () => void }) {
  const [hov, setHov] = createSignal(false)
  return (
    <button
      onClick={props.onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        display: "flex",
        "align-items": "center",
        gap: props.active ? "6px" : "0",
        padding: props.active ? "5px 10px" : "5px 8px",
        "border-radius": "8px",
        cursor: "pointer",
        color: props.active || hov() ? "#e8e8e8" : "#888",
        "font-size": "13px",
        "font-weight": "500",
        background: props.active ? "#2e2e2e" : hov() ? "#2a2a2a" : "transparent",
        border: "none",
        transition: "background .15s, color .15s",
      }}
    >
      {props.icon}
      <Show when={props.active}>
        <span style={{ "font-size": "13px" }}>{props.label}</span>
      </Show>
    </button>
  )
}

// ─── Nav item ────────────────────────────────────────────────────────────────
function NavItem(props: { icon: JSX.Element; label: string; onClick?: () => void; accent?: boolean }) {
  const [hov, setHov] = createSignal(false)
  return (
    <div
      onClick={props.onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        display: "flex",
        "align-items": "center",
        gap: "10px",
        padding: "7px 10px",
        "border-radius": "8px",
        cursor: "pointer",
        color: hov() ? "#e8e8e8" : "#c8c8c8",
        "font-size": "13.5px",
        transition: "background .12s, color .12s",
        background: hov() ? "#262626" : "transparent",
      }}
    >
      <span style={{ color: props.accent ? "#a78bfa" : "#888", display: "flex" }}>{props.icon}</span>
      <span>{props.label}</span>
    </div>
  )
}

// ─── Section header ──────────────────────────────────────────────────────────
function SectionLabel(props: { label: string }) {
  return (
    <div
      style={{
        "font-size": "10.5px",
        "font-weight": "600",
        color: "#555",
        "letter-spacing": "0.06em",
        "text-transform": "uppercase",
        padding: "8px 12px 4px",
      }}
    >
      {props.label}
    </div>
  )
}

// ─── Collapsed rail ──────────────────────────────────────────────────────────
function CollapsedRail(props: { onToggle: () => void }) {
  const [hov, setHov] = createSignal(false)
  return (
    <div
      style={{
        width: "48px",
        height: "100%",
        background: "#1c1c1c",
        display: "flex",
        "flex-direction": "column",
        "align-items": "center",
        "padding-top": "12px",
      }}
    >
      <button
        title="Open sidebar"
        onClick={props.onToggle}
        onMouseEnter={() => setHov(true)}
        onMouseLeave={() => setHov(false)}
        style={{
          width: "32px",
          height: "32px",
          "border-radius": "7px",
          display: "flex",
          "align-items": "center",
          "justify-content": "center",
          color: hov() ? "#e8e8e8" : "#888",
          cursor: "pointer",
          background: hov() ? "#2a2a2a" : "transparent",
          border: "none",
          transition: "background .15s, color .15s",
          padding: "0",
        }}
      >
        <IconSidebar />
      </button>
    </div>
  )
}

// ─── Empty-state hint ────────────────────────────────────────────────────────
function EmptyHint(props: { label: string }) {
  return (
    <div
      style={{
        padding: "14px 14px",
        color: "#444",
        "font-size": "12.5px",
        "text-align": "center",
        "line-height": "1.5",
      }}
    >
      {props.label}
    </div>
  )
}

// ─── Pinned entity row ───────────────────────────────────────────────────────
function PinnedEntityRow(props: {
  entity: { type: TabType; id: string; title: string }
  onUnpin: () => void
  onClick: () => void
}) {
  const [hov, setHov] = createSignal(false)
  const typeLabel = () => props.entity.type === "chat" ? "💬" : props.entity.type === "code" ? "⌨️" : "👥"
  return (
    <div
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      onClick={props.onClick}
      style={{
        display: "flex",
        "align-items": "center",
        gap: "6px",
        padding: "5px 8px",
        "border-radius": "6px",
        cursor: "pointer",
        background: hov() ? "#262626" : "transparent",
        transition: "background .12s",
      }}
    >
      <span style={{ "font-size": "12px", "flex-shrink": "0" }}>{typeLabel()}</span>
      <span style={{ flex: "1", "font-size": "12.5px", color: "#c8c8c8", overflow: "hidden", "text-overflow": "ellipsis", "white-space": "nowrap" }}>
        {props.entity.title}
      </span>
      <Show when={hov()}>
        <button
          onClick={(e) => { e.stopPropagation(); props.onUnpin() }}
          style={{ "font-size": "10px", color: "#555", border: "none", background: "transparent", cursor: "pointer", padding: "0 2px", "flex-shrink": "0" }}
        >✕</button>
      </Show>
    </div>
  )
}

// ─── Pinned entities section (shown above session list in each tab) ───────────
function PinnedEntitiesSection(props: {
  pinnedStore: ReturnType<typeof usePinnedStore>
  currentTab: TabType
  navigate: ReturnType<typeof useNavigate>
  params: { dir?: string }
}) {
  // Show ALL pinned entities (cross-tab) — with tab type label for context
  const entities = () => props.pinnedStore.pinnedEntities()
  return (
    <Show when={entities().length > 0}>
      <div style={{ "margin-bottom": "4px" }}>
        <div
          style={{
            "font-size": "10.5px",
            "font-weight": "600",
            color: "#555",
            "letter-spacing": "0.06em",
            "text-transform": "uppercase",
            padding: "8px 12px 2px",
          }}
        >
          📌 Pinned
        </div>
        <div style={{ padding: "0 4px" }}>
          <For each={entities()}>
            {(entity) => (
              <PinnedEntityRow
                entity={entity}
                onUnpin={() => props.pinnedStore.unpinEntity(entity.id)}
                onClick={() => {
                  const dir = props.params.dir
                  if (dir) props.navigate(`/${dir}/session/${entity.id}`)
                }}
              />
            )}
          </For>
        </div>
        <div style={{ height: "1px", background: "#282828", margin: "6px 0" }} />
      </div>
    </Show>
  )
}

// ─── Main SidebarContent component ──────────────────────────────────────────
export const SidebarContent = (props: {
  mobile?: boolean
  opened: Accessor<boolean>
  aimMove: (event: MouseEvent) => void
  projects: Accessor<LocalProject[]>
  renderProject: (project: LocalProject) => JSX.Element
  handleDragStart: (event: unknown) => void
  handleDragEnd: () => void
  handleDragOver: (event: DragEvent) => void
  openProjectLabel: JSX.Element
  openProjectKeybind: Accessor<string | undefined>
  onOpenProject: () => void
  renderProjectOverlay: () => JSX.Element
  settingsLabel: Accessor<string>
  settingsKeybind: Accessor<string | undefined>
  onOpenSettings: () => void
  helpLabel: Accessor<string>
  onOpenHelp: () => void
  /** renderPanel now accepts a filter fn so each tab can show only its own sessions */
  renderPanel: (filter: (id: string) => boolean) => JSX.Element
  onNewSession: (type: TabType) => void
}): JSX.Element => {
  const layout = useLayout()
  const sessionType = useSessionType()
  const pinnedStore = usePinnedStore()
  const navigate = useNavigate()
  const params = useParams()

  // Track last active session per tab so switching tabs navigates to the right session
  const TAB_SESSION_KEY = "ultron:last-session-per-tab"
  const loadTabSessions = (): Record<TabType, string | null> => {
    try { return JSON.parse(localStorage.getItem(TAB_SESSION_KEY) ?? "{}") } catch { return {} as Record<TabType, string | null> }
  }
  const saveTabSession = (type: TabType, id: string) => {
    try {
      const m = loadTabSessions()
      m[type] = id
      localStorage.setItem(TAB_SESSION_KEY, JSON.stringify(m))
    } catch {}
  }

  type SidebarTab = TabType | "agents"
  const [tab, setTab] = createSignal<SidebarTab>("code")

  // When the active session changes (params.id), record it under the current tab.
  // Skip virtual tab-marker IDs (__tab_X__) — those just indicate the new-session screen.
  createEffect(() => {
    const id = params.id
    if (!id || id.startsWith("__tab_")) return
    const t = sessionType.get(id)
    // Update current tab to match the open session's type
    setTab(t)
    saveTabSession(t, id)
  })

  const switchTab = (newTab: SidebarTab) => {
    const currentTab = tab()
    if (currentTab === newTab) return
    setTab(newTab)
    if (newTab === "agents") return // Agents tab is self-contained, no navigation
    const dir = params.dir
    if (!dir) return
    // Navigate to the last session of this tab, or to the per-tab virtual route
    const lastSessions = loadTabSessions()
    const lastId = lastSessions[newTab as TabType]
    if (lastId) {
      navigate(`/${dir}/session/${lastId}`)
    } else {
      // No previous real session — navigate to a per-tab virtual route so each tab
      // gets its own prompt cache entry and inputs stay isolated.
      try { sessionStorage.setItem("ultron:pending-session-type", newTab) } catch {}
      navigate(`/${dir}/session/__tab_${newTab as TabType}__`)
    }
  }

  const toggle = () => layout.sidebar.toggle()

  return (
    <Show
      when={props.opened() || props.mobile}
      fallback={<CollapsedRail onToggle={toggle} />}
    >
      <div
        style={{
          display: "flex",
          "flex-direction": "column",
          width: "100%",
          height: "100%",
          background: "#1c1c1c",
          color: "#e8e8e8",
          "font-size": "14px",
          overflow: "hidden",
        }}
      >
        {/* ── Top nav ── */}
        <div
          style={{
            display: "flex",
            "align-items": "center",
            padding: "12px 14px",
            gap: "2px",
            "flex-shrink": "0",
          }}
        >
          <NavBtn title="Close sidebar" onClick={toggle}>
            <IconSidebar />
          </NavBtn>
          <NavBtn title="Search">
            <IconSearch />
          </NavBtn>
          <div style={{ flex: "1" }} />
          <NavBtn title="Back" onClick={() => window.history.back()}>
            <IconBack />
          </NavBtn>
          <NavBtn title="Forward" onClick={() => window.history.forward()}>
            <IconForward />
          </NavBtn>
        </div>

        {/* ── Session toolbar (Search + actions injected here via Portal) ── */}
        <div
          style={{
            padding: "4px 10px 2px",
            "flex-shrink": "0",
            display: "flex",
            "flex-direction": "column",
            gap: "4px",
          }}
        >
          <div id="ultron-sidebar-search" style={{ width: "100%" }} />
          <div
            id="ultron-sidebar-toolbar"
            style={{ display: "flex", "align-items": "center", gap: "4px", "flex-wrap": "wrap" }}
          />
        </div>

        {/* ── Tab bar ── */}
        <div
          style={{
            display: "flex",
            "align-items": "center",
            padding: "4px 10px 8px",
            gap: "2px",
            "flex-shrink": "0",
          }}
        >
          <TabBtn active={tab() === "chat"} label="Chat" icon={<IconChat />} onClick={() => switchTab("chat")} />
          <TabBtn active={tab() === "code"} label="Code" icon={<IconCode />} onClick={() => switchTab("code")} />
          <TabBtn active={tab() === "cowork"} label="Cowork" icon={<IconCowork />} onClick={() => switchTab("cowork")} />
          <TabBtn active={tab() === "agents"} label="Swarm" icon={<IconAgents />} onClick={() => switchTab("agents")} />
        </div>

        {/* ── Tab-specific quick actions ── */}
        <Show when={tab() === "chat"}>
          <div style={{ padding: "0 8px 4px", "flex-shrink": "0" }}>
            <NavItem icon={<IconPlus />} label="New chat" accent onClick={() => props.onNewSession("chat")} />
            <NavItem icon={<IconFolder />} label="Projects" onClick={props.onOpenProject} />
            <NavItem icon={<IconStar />} label="Artifacts" />
            <NavItem icon={<IconPen />} label="Customize" onClick={props.onOpenSettings} />
          </div>
          <div style={{ height: "1px", background: "#282828", margin: "4px 0", "flex-shrink": "0" }} />
        </Show>

        <Show when={tab() === "code"}>
          <div style={{ padding: "0 8px 4px", "flex-shrink": "0" }}>
            <NavItem icon={<IconPlus />} label="New session" accent onClick={() => props.onNewSession("code")} />
          </div>
          <div style={{ height: "1px", background: "#282828", margin: "4px 0", "flex-shrink": "0" }} />
        </Show>

        <Show when={tab() === "cowork"}>
          <div style={{ padding: "0 8px 4px", "flex-shrink": "0" }}>
            <NavItem icon={<IconPlus />} label="New task" accent onClick={() => props.onNewSession("cowork")} />
          </div>
          <div style={{ height: "1px", background: "#282828", margin: "4px 0", "flex-shrink": "0" }} />
        </Show>

        <Show when={tab() === "agents"}>
          <div style={{ height: "1px", background: "#282828", margin: "4px 0", "flex-shrink": "0" }} />
        </Show>

        {/* ── Scrollable area ── */}
        <div
          style={{
            flex: "1",
            "overflow-y": "auto",
            "overflow-x": "hidden",
            "min-height": "0",
          }}
          class="[&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:rounded [&::-webkit-scrollbar-thumb]:bg-[#333] hover:[&::-webkit-scrollbar-thumb]:bg-[#444]"
        >
          {/* Chat history */}
          <Show when={tab() === "chat"}>
            <div style={{ padding: "0 4px" }}>
              <PinnedEntitiesSection
                pinnedStore={pinnedStore}
                currentTab="chat"
                navigate={navigate}
                params={params}
              />
              <SectionLabel label="Recent Chats" />
              {props.renderPanel((id) => sessionType.get(id) === "chat")}
            </div>
          </Show>

          {/* Code history */}
          <Show when={tab() === "code"}>
            <div style={{ padding: "0 4px" }}>
              <PinnedEntitiesSection
                pinnedStore={pinnedStore}
                currentTab="code"
                navigate={navigate}
                params={params}
              />
              <SectionLabel label="Code Sessions" />
              {props.renderPanel((id) => {
                const t = sessionType.get(id)
                return t === "code"
              })}
            </div>
          </Show>

          {/* Cowork tasks */}
          <Show when={tab() === "cowork"}>
            <div style={{ padding: "0 4px" }}>
              <PinnedEntitiesSection
                pinnedStore={pinnedStore}
                currentTab="cowork"
                navigate={navigate}
                params={params}
              />
              <SectionLabel label="Cowork Tasks" />
              {props.renderPanel((id) => sessionType.get(id) === "cowork")}
            </div>
          </Show>

          {/* Agents / Swarm panel */}
          <Show when={tab() === "agents"}>
            <SwarmPanel />
          </Show>
        </div>

        {/* ── Bottom: cross-context hint ── */}
        <div
          style={{
            "flex-shrink": "0",
            padding: "6px 12px",
            "border-top": "1px solid #222",
          }}
        >
          {/* Cross-context tip */}
          <div
            style={{
              display: "flex",
              "align-items": "center",
              gap: "6px",
              padding: "4px 6px",
              "border-radius": "6px",
              "font-size": "11.5px",
              color: "#555",
              cursor: "default",
            }}
            title="In any session, type '@chat', '@code', or '@cowork' to reference context from another tab"
          >
            <span style={{ display: "flex", color: "#444" }}>
              <IconLink />
            </span>
            Cross-tab context: mention @chat / @code / @cowork in any message
          </div>
        </div>

        {/* ── User bar ── */}
        <div style={{ "flex-shrink": "0", padding: "4px 8px 8px" }}>
          <div
            style={{
              display: "flex",
              "align-items": "center",
              gap: "10px",
              padding: "6px 10px",
              "border-radius": "8px",
              cursor: "pointer",
            }}
          >
            <span style={{ color: "#888", display: "flex" }}>
              <IconUser />
            </span>
            <span style={{ flex: "1", "font-size": "13.5px", color: "#c8c8c8" }}>Moez</span>
            <span style={{ color: "#888", display: "flex" }}>
              <IconChevronRight />
            </span>
          </div>
        </div>
      </div>
    </Show>
  )
}
