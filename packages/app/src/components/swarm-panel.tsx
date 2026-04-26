/**
 * Ultron Swarm Panel
 * Connects via WebSocket (/ws) for real-time updates.
 * Falls back to polling /snapshot every 3 seconds if WS unavailable.
 *
 * Panels:
 *   Agents    — live agent cards with skills, status, spawn/kill/pause/assign
 *   Tasks     — color-coded task list from SQLite
 *   DAG       — task dependency graph (SVG)
 *   Bus       — agent communication log
 *   Submit    — send a task to swarm
 */
import {
  createSignal, createEffect, createMemo, For, Show, onCleanup,
  type JSX, batch,
} from "solid-js"
import { createStore } from "solid-js/store"

const ORCH_HTTP = "http://127.0.0.1:5000"
const ORCH_WS   = "ws://127.0.0.1:5000/ws"
const POLL_MS   = 3500

// ── Types ─────────────────────────────────────────────────────────────────────

type AgentInfo = {
  port: number; alive?: boolean; pid?: number | null
  last_hb?: number | null; missed?: number; retries?: number
  skills?: string[]; status?: string; current_task?: string | null
  spawned?: boolean
}

type Task = {
  id: number; description: string; assigned_agent: string
  status: "queued" | "running" | "done" | "failed" | "assigned" | "pending" | "ready"
  created_at: number; completed_at?: number | null
  retry_count?: number; result?: string | null
}

type DAGNode = {
  id: string; description: string; required_skills: string[]
  status: string; assigned_agent?: string | null
  result?: string | null; error?: string | null
  created_at?: number; completed_at?: number | null
}

type DAGEdge = { from: string; to: string }

type BusEntry = {
  ts: number; channel: string; event?: string; agent?: string; task_id?: string
  description?: string
}

type Snapshot = {
  agents: Record<string, AgentInfo>
  tasks: Task[]
  dag: { nodes: DAGNode[]; edges: DAGEdge[] }
  bus_log: BusEntry[]
}

// ── Styles ────────────────────────────────────────────────────────────────────

const card: JSX.CSSProperties = {
  background: "#1e1e1e", border: "1px solid #2a2a2a",
  "border-radius": "8px", padding: "10px 12px", "margin-bottom": "6px",
}
const badge = (color: string): JSX.CSSProperties => ({
  background: color + "22", color,
  "border-radius": "4px", padding: "1px 6px",
  "font-size": "10.5px", "font-weight": "600",
})
const btn = (color = "#555"): JSX.CSSProperties => ({
  background: color + "22", color, border: `1px solid ${color}44`,
  "border-radius": "4px", padding: "2px 8px", "font-size": "11px",
  cursor: "pointer", "font-weight": "500",
})

// ── Helpers ───────────────────────────────────────────────────────────────────

function relTime(ts: number | null | undefined): string {
  if (!ts) return "—"
  const s = Math.floor(Date.now() / 1000 - ts)
  if (s < 60) return `${s}s ago`
  if (s < 3600) return `${Math.floor(s / 60)}m ago`
  return `${Math.floor(s / 3600)}h ago`
}

const STATUS_COLOR: Record<string, string> = {
  done: "#4ade80", running: "#60a5fa", failed: "#f87171",
  queued: "#888", assigned: "#a78bfa", pending: "#888", ready: "#facc15",
  idle: "#4ade80", busy: "#60a5fa", paused: "#facc15", offline: "#f87171",
}
const sc = (s: string) => STATUS_COLOR[s] ?? "#888"

const AGENT_ICONS: Record<string, string> = {
  planner: "🗺", designer: "🎨", builder: "🔨",
  debugger: "🐛", verifier: "✅", researcher: "🔬", coder: "💻",
}
const agentIcon = (name: string) =>
  AGENT_ICONS[name] ?? (name.includes("spawn") ? "⚡" : "🤖")

function Label(props: { children: JSX.Element }) {
  return (
    <div style={{
      "font-size": "10.5px", "font-weight": "600", color: "#555",
      "letter-spacing": "0.06em", "text-transform": "uppercase",
      padding: "10px 0 4px",
    }}>
      {props.children}
    </div>
  )
}

// ── HTTP helpers ──────────────────────────────────────────────────────────────

async function post(path: string, body?: object): Promise<boolean> {
  try {
    const r = await fetch(`${ORCH_HTTP}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    })
    return r.ok
  } catch {
    return false
  }
}

// ── Spawn Agent dialog ────────────────────────────────────────────────────────

function SpawnDialog(props: { onClose: () => void; onSpawn: (name: string, skills: string[]) => void }) {
  const [name, setName] = createSignal("")
  const [skills, setSkills] = createSignal("code")
  return (
    <div style={{
      position: "fixed", inset: "0", background: "#00000088",
      display: "flex", "align-items": "center", "justify-content": "center",
      "z-index": "1000",
    }}>
      <div style={{ ...card, width: "320px", "margin-bottom": "0" }}>
        <div style={{ "font-size": "13px", "font-weight": "600", color: "#e8e8e8", "margin-bottom": "10px" }}>
          ⚡ Spawn New Agent
        </div>
        <div style={{ "margin-bottom": "8px" }}>
          <div style={{ "font-size": "11px", color: "#888", "margin-bottom": "3px" }}>Name (optional)</div>
          <input
            style={{
              width: "100%", background: "#252525", border: "1px solid #333",
              "border-radius": "5px", color: "#e8e8e8", padding: "5px 8px",
              "font-size": "12px", "box-sizing": "border-box",
            }}
            placeholder="e.g. my_coder"
            value={name()}
            onInput={(e) => setName(e.currentTarget.value)}
          />
        </div>
        <div style={{ "margin-bottom": "10px" }}>
          <div style={{ "font-size": "11px", color: "#888", "margin-bottom": "3px" }}>Skills (comma-separated)</div>
          <input
            style={{
              width: "100%", background: "#252525", border: "1px solid #333",
              "border-radius": "5px", color: "#e8e8e8", padding: "5px 8px",
              "font-size": "12px", "box-sizing": "border-box",
            }}
            placeholder="e.g. code,debug,verify"
            value={skills()}
            onInput={(e) => setSkills(e.currentTarget.value)}
          />
        </div>
        <div style={{ display: "flex", gap: "6px" }}>
          <button
            onClick={() => {
              const skillList = skills().split(",").map(s => s.trim()).filter(Boolean)
              if (skillList.length) props.onSpawn(name(), skillList)
            }}
            style={{ ...btn("#a78bfa"), flex: "1", padding: "6px" }}
          >Spawn</button>
          <button onClick={props.onClose} style={{ ...btn(), flex: "0 0 auto", padding: "6px 12px" }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}

// ── Assign Task dialog ────────────────────────────────────────────────────────

function AssignDialog(props: {
  agentName: string
  onClose: () => void
  onAssign: (desc: string) => void
}) {
  const [desc, setDesc] = createSignal("")
  return (
    <div style={{
      position: "fixed", inset: "0", background: "#00000088",
      display: "flex", "align-items": "center", "justify-content": "center",
      "z-index": "1000",
    }}>
      <div style={{ ...card, width: "380px", "margin-bottom": "0" }}>
        <div style={{ "font-size": "13px", "font-weight": "600", color: "#e8e8e8", "margin-bottom": "10px" }}>
          📋 Assign Task → {props.agentName}
        </div>
        <textarea
          rows={3}
          placeholder="Describe the task…"
          style={{
            width: "100%", background: "#252525", border: "1px solid #333",
            "border-radius": "5px", color: "#e8e8e8", padding: "6px 8px",
            "font-size": "12px", resize: "none", "box-sizing": "border-box",
          }}
          value={desc()}
          onInput={(e) => setDesc(e.currentTarget.value)}
        />
        <div style={{ display: "flex", gap: "6px", "margin-top": "8px" }}>
          <button
            onClick={() => { if (desc().trim()) props.onAssign(desc().trim()) }}
            style={{ ...btn("#60a5fa"), flex: "1", padding: "6px" }}
          >Assign</button>
          <button onClick={props.onClose} style={{ ...btn(), flex: "0 0 auto", padding: "6px 12px" }}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}

// ── Agent Card ────────────────────────────────────────────────────────────────

function AgentCard(props: {
  name: string
  info: AgentInfo
  onKill: () => void
  onPause: () => void
  onAssign: () => void
}) {
  const [hov, setHov] = createSignal(false)
  const status  = () => props.info.status ?? (props.info.alive ? "idle" : "offline")
  const color   = () => sc(status())
  const skills  = () => props.info.skills ?? []
  return (
    <div style={{ ...card }}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
    >
      <div style={{ display: "flex", "align-items": "center", gap: "8px" }}>
        <span style={{ "font-size": "18px" }}>{agentIcon(props.name)}</span>
        <div style={{ flex: "1", "min-width": "0" }}>
          <div style={{ "font-size": "13px", "font-weight": "600", color: "#e8e8e8", "text-transform": "capitalize" }}>
            {props.name}
            <Show when={props.info.spawned}>
              <span style={{ ...badge("#facc15"), "margin-left": "6px" }}>spawned</span>
            </Show>
          </div>
          <div style={{ "font-size": "11px", color: "#666" }}>
            port {props.info.port} · pid {props.info.pid ?? "—"}
          </div>
        </div>
        <div style={{
          width: "8px", height: "8px", "border-radius": "50%",
          background: color(), "flex-shrink": "0",
        }} />
      </div>

      {/* Skills */}
      <Show when={skills().length > 0}>
        <div style={{ "margin-top": "5px", display: "flex", gap: "3px", "flex-wrap": "wrap" }}>
          <For each={skills()}>
            {(s) => <span style={badge("#a78bfa")}>{s}</span>}
          </For>
        </div>
      </Show>

      {/* Status badges */}
      <div style={{ "margin-top": "5px", display: "flex", gap: "4px", "flex-wrap": "wrap" }}>
        <span style={badge(color())}>{status()}</span>
        <Show when={(props.info.missed ?? 0) > 0}>
          <span style={badge("#facc15")}>{props.info.missed} missed hb</span>
        </Show>
        <Show when={(props.info.retries ?? 0) > 0}>
          <span style={badge("#f87171")}>restarted ×{props.info.retries}</span>
        </Show>
        <span style={badge("#555")}>hb {relTime(props.info.last_hb)}</span>
      </div>

      {/* Current task */}
      <Show when={props.info.current_task}>
        <div style={{ "margin-top": "5px", "font-size": "11px", color: "#60a5fa",
          overflow: "hidden", "text-overflow": "ellipsis", "white-space": "nowrap" }}>
          → {props.info.current_task}
        </div>
      </Show>

      {/* Control buttons — show on hover */}
      <Show when={hov()}>
        <div style={{ "margin-top": "7px", display: "flex", gap: "5px" }}>
          <button onClick={props.onAssign} style={btn("#60a5fa")}>📋 Assign</button>
          <button onClick={props.onPause}  style={btn("#facc15")}>
            {status() === "paused" ? "▶ Resume" : "⏸ Pause"}
          </button>
          <button onClick={props.onKill}   style={btn("#f87171")}>✕ Kill</button>
        </div>
      </Show>
    </div>
  )
}

// ── Task Row ──────────────────────────────────────────────────────────────────

function TaskRow(props: { task: Task }) {
  const t   = props.task
  const col = () => sc(t.status)
  return (
    <div style={{ ...card, padding: "8px 12px" }}>
      <div style={{ display: "flex", "align-items": "flex-start", gap: "8px" }}>
        <span style={{ ...badge(col()), "flex-shrink": "0", "margin-top": "1px" }}>{t.status}</span>
        <div style={{ flex: "1", "min-width": "0" }}>
          <div style={{ "font-size": "12px", color: "#d4d4d4",
            overflow: "hidden", "text-overflow": "ellipsis", "white-space": "nowrap" }}>
            {t.description}
          </div>
          <div style={{ "font-size": "10.5px", color: "#555", "margin-top": "2px" }}>
            {t.assigned_agent} · {relTime(t.created_at)}
          </div>
        </div>
      </div>
      <Show when={t.result && t.status === "done"}>
        <div style={{ "margin-top": "5px", "font-size": "11px", color: "#777",
          "white-space": "pre-wrap", "word-break": "break-word",
          "max-height": "40px", overflow: "hidden" }}>
          {(t.result ?? "").slice(0, 150)}{(t.result?.length ?? 0) > 150 ? "…" : ""}
        </div>
      </Show>
    </div>
  )
}

// ── DAG SVG Visualization ─────────────────────────────────────────────────────

function DAGView(props: { nodes: DAGNode[]; edges: DAGEdge[] }) {
  // Simple grid layout: nodes in rows of 3
  const W = 160, H = 52, GAP_X = 24, GAP_Y = 30, COLS = 3
  const PX = (i: number) => (i % COLS) * (W + GAP_X) + 12
  const PY = (i: number) => Math.floor(i / COLS) * (H + GAP_Y) + 12

  const posMap = createMemo(() => {
    const m: Record<string, { x: number; y: number }> = {}
    props.nodes.forEach((n, i) => { m[n.id] = { x: PX(i), y: PY(i) } })
    return m
  })

  const svgW = createMemo(() => Math.max(COLS * (W + GAP_X) + 24, 400))
  const svgH = createMemo(() => {
    const rows = Math.ceil(props.nodes.length / COLS)
    return rows * (H + GAP_Y) + 24
  })

  return (
    <div style={{ "overflow-x": "auto", "overflow-y": "auto", "max-height": "220px" }}>
      <Show when={props.nodes.length === 0}>
        <div style={{ color: "#444", "font-size": "12px", padding: "12px 0" }}>
          No DAG tasks yet — submit a task to see the graph
        </div>
      </Show>
      <Show when={props.nodes.length > 0}>
        <svg
          width={svgW()}
          height={svgH()}
          style={{ display: "block" }}
        >
          {/* Edges */}
          <For each={props.edges}>
            {(e) => {
              const from = posMap()[e.from]
              const to   = posMap()[e.to]
              if (!from || !to) return null
              const x1 = from.x + W / 2
              const y1 = from.y + H
              const x2 = to.x + W / 2
              const y2 = to.y
              const mx = (x1 + x2) / 2
              return (
                <path
                  d={`M${x1},${y1} C${x1},${mx} ${x2},${mx} ${x2},${y2}`}
                  fill="none"
                  stroke="#444"
                  stroke-width="1.5"
                  marker-end="url(#arrowhead)"
                />
              )
            }}
          </For>

          {/* Arrow marker */}
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6"
              refX="6" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" fill="#555" />
            </marker>
          </defs>

          {/* Nodes */}
          <For each={props.nodes}>
            {(n, i) => {
              const x = PX(i())
              const y = PY(i())
              const col = sc(n.status)
              const desc = n.description.length > 22
                ? n.description.slice(0, 22) + "…"
                : n.description
              const agent = n.assigned_agent ?? ""
              return (
                <>
                  <rect x={x} y={y} width={W} height={H}
                    rx="5" fill="#1e1e1e" stroke={col} stroke-width="1.5" />
                  <text x={x + 8} y={y + 16} fill="#e8e8e8" font-size="11" font-family="monospace">
                    {desc}
                  </text>
                  <text x={x + 8} y={y + 30} fill={col} font-size="10" font-family="monospace">
                    {n.status}
                  </text>
                  <Show when={agent}>
                    <text x={x + 8} y={y + 44} fill="#666" font-size="9.5" font-family="monospace">
                      {agent}
                    </text>
                  </Show>
                </>
              )
            }}
          </For>
        </svg>
      </Show>
    </div>
  )
}

// ── Bus Log ───────────────────────────────────────────────────────────────────

function BusLog(props: { entries: BusEntry[] }) {
  return (
    <div style={{ "max-height": "160px", "overflow-y": "auto" }}>
      <Show when={props.entries.length === 0}>
        <div style={{ color: "#444", "font-size": "11.5px" }}>No messages yet</div>
      </Show>
      <For each={props.entries.slice(-30).reverse()}>
        {(e) => {
          const ts  = new Date(e.ts * 1000).toLocaleTimeString()
          const col = e.channel.startsWith("skill.") ? "#a78bfa"
            : e.channel.startsWith("agent.") ? "#60a5fa" : "#888"
          return (
            <div style={{ "font-size": "11px", color: "#888", padding: "2px 0",
              "border-bottom": "1px solid #1a1a1a" }}>
              <span style={{ color: "#555", "margin-right": "5px" }}>{ts}</span>
              <span style={{ color: col }}>[{e.channel}]</span>
              {" "}{e.event ?? ""}{" "}
              <span style={{ color: "#666" }}>{e.agent ?? e.task_id ?? ""}</span>
            </div>
          )
        }}
      </For>
    </div>
  )
}

// ── Submit Form ───────────────────────────────────────────────────────────────

function SubmitForm(props: { agents: string[] }) {
  const [desc,    setDesc]    = createSignal("")
  const [agent,   setAgent]   = createSignal("planner")
  const [skills,  setSkills]  = createSignal("")
  const [sending, setSending] = createSignal(false)
  const [msg,     setMsg]     = createSignal<{ ok: boolean; text: string } | null>(null)

  const submit = async () => {
    if (!desc().trim()) return
    setSending(true); setMsg(null)
    try {
      const r = await fetch(`${ORCH_HTTP}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: desc(), target_agent: agent() }),
      })
      const data = await r.json() as { ok: boolean; task_id?: string; error?: string }
      if (data.ok) {
        setMsg({ ok: true, text: `Submitted ✓ (id: ${data.task_id})` })
        setDesc("")
      } else {
        setMsg({ ok: false, text: data.error ?? "Error" })
      }
    } catch {
      setMsg({ ok: false, text: "Cannot reach swarm" })
    } finally {
      setSending(false)
    }
  }

  const submitDAG = async () => {
    if (!desc().trim()) return
    setSending(true); setMsg(null)
    try {
      const skillList = skills().split(",").map(s => s.trim()).filter(Boolean)
      const r = await fetch(`${ORCH_HTTP}/dag/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          description: desc(),
          skills: skillList.length ? skillList : ["plan"],
        }),
      })
      const data = await r.json() as { ok: boolean; task_id?: string; error?: string }
      if (data.ok) {
        setMsg({ ok: true, text: `DAG task ✓ (id: ${data.task_id})` })
        setDesc("")
      } else {
        setMsg({ ok: false, text: data.error ?? "Error" })
      }
    } catch {
      setMsg({ ok: false, text: "Cannot reach swarm" })
    } finally {
      setSending(false)
    }
  }

  const inputStyle: JSX.CSSProperties = {
    width: "100%", background: "#252525", border: "1px solid #333",
    "border-radius": "6px", color: "#e8e8e8", "font-size": "12.5px",
    padding: "7px 10px", resize: "none", outline: "none",
    "font-family": "inherit", "box-sizing": "border-box",
  }

  return (
    <div style={{ ...card, "margin-bottom": "0" }}>
      <div style={{ "font-size": "11px", color: "#666", "margin-bottom": "6px",
        "font-weight": "600", "text-transform": "uppercase", "letter-spacing": "0.05em" }}>
        Submit Task
      </div>
      <textarea rows={3} placeholder="Describe the task…"
        style={inputStyle}
        value={desc()}
        onInput={(e) => setDesc(e.currentTarget.value)}
        onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) submit() }}
      />
      {/* Skills row for DAG submit */}
      <input
        placeholder="Skills (comma-sep, for DAG route): code,verify"
        style={{ ...inputStyle, "margin-top": "5px", resize: undefined }}
        value={skills()}
        onInput={(e) => setSkills(e.currentTarget.value)}
      />
      <div style={{ display: "flex", gap: "6px", "margin-top": "6px", "align-items": "center" }}>
        <select
          style={{ ...inputStyle, padding: "5px 8px", flex: "0 0 auto", width: "auto" }}
          value={agent()}
          onChange={(e) => setAgent(e.currentTarget.value)}
        >
          <For each={props.agents}>
            {(a) => <option value={a}>{a}</option>}
          </For>
        </select>
        <button
          disabled={sending() || !desc().trim()}
          onClick={submit}
          style={{
            flex: "1", background: sending() ? "#333" : "#a78bfa",
            color: "#fff", border: "none", "border-radius": "6px",
            padding: "6px 12px", "font-size": "12.5px",
            cursor: sending() ? "not-allowed" : "pointer", "font-weight": "600",
          }}
        >{sending() ? "Sending…" : "Queue ⌘↵"}</button>
        <button
          disabled={sending() || !desc().trim()}
          onClick={submitDAG}
          style={{
            flex: "1", background: sending() ? "#333" : "#4ade8044",
            color: "#4ade80", border: "1px solid #4ade8033", "border-radius": "6px",
            padding: "6px 12px", "font-size": "12.5px",
            cursor: sending() ? "not-allowed" : "pointer", "font-weight": "600",
          }}
        >DAG Route</button>
      </div>
      <Show when={msg()}>
        {(m) => (
          <div style={{ "margin-top": "5px", "font-size": "11.5px",
            color: m().ok ? "#4ade80" : "#f87171" }}>{m().text}</div>
        )}
      </Show>
    </div>
  )
}

// ── Section toggle ────────────────────────────────────────────────────────────

function Section(props: { title: string; default?: boolean; children: JSX.Element }) {
  const [open, setOpen] = createSignal(props.default !== false)
  return (
    <div>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: "100%", background: "transparent", border: "none",
          "border-bottom": "1px solid #282828", color: "#555",
          "font-size": "10.5px", "font-weight": "600", "letter-spacing": "0.06em",
          "text-transform": "uppercase", padding: "8px 0 4px",
          cursor: "pointer", "text-align": "left",
          display: "flex", "align-items": "center", gap: "6px",
        }}
      >
        <span>{open() ? "▾" : "▸"}</span>
        {props.title}
      </button>
      <Show when={open()}>{props.children}</Show>
    </div>
  )
}

// ── Main SwarmPanel ───────────────────────────────────────────────────────────

export function SwarmPanel(): JSX.Element {
  const [snap, setSnap] = createStore<{
    data: Snapshot | null; error: string | null; loading: boolean; wsConnected: boolean
  }>({ data: null, error: null, loading: true, wsConnected: false })

  const [showSpawn,  setShowSpawn]  = createSignal(false)
  const [assignAgent, setAssignAgent] = createSignal<string | null>(null)

  // ── WebSocket connection ────────────────────────────────────────────────────

  let ws: WebSocket | null = null
  let pollTimer: ReturnType<typeof setInterval> | null = null

  const fetchSnapshot = async () => {
    try {
      const r = await fetch(`${ORCH_HTTP}/snapshot`, { signal: AbortSignal.timeout(4000) })
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      const data = await r.json() as Snapshot
      setSnap({ data, error: null, loading: false })
    } catch (e) {
      setSnap({ error: (e as Error).message, loading: false })
    }
  }

  const connectWS = () => {
    try {
      ws = new WebSocket(ORCH_WS)
      ws.onopen = () => {
        setSnap("wsConnected", true)
        // Stop polling when WS is up
        if (pollTimer) { clearInterval(pollTimer); pollTimer = null }
      }
      ws.onmessage = (ev) => {
        try {
          const msg = JSON.parse(ev.data as string) as { type: string; data?: Snapshot }
          if (msg.type === "init" && msg.data) {
            setSnap({ data: msg.data, error: null, loading: false })
          } else if (msg.type === "snapshot" && msg.data) {
            setSnap("data", msg.data)
          }
          // Push "ping" to keep alive
          if (ws?.readyState === WebSocket.OPEN) ws.send("ping")
        } catch {}
      }
      ws.onclose = () => {
        setSnap("wsConnected", false)
        ws = null
        // Fall back to polling
        if (!pollTimer) {
          void fetchSnapshot()
          pollTimer = setInterval(() => void fetchSnapshot(), POLL_MS)
        }
        // Reconnect in 5s
        setTimeout(connectWS, 5000)
      }
      ws.onerror = () => ws?.close()
    } catch {
      // WS not available — fall through to polling
    }
  }

  createEffect(() => {
    connectWS()
    // Always start polling as fallback; WS onopen will clear it
    void fetchSnapshot()
    pollTimer = setInterval(() => void fetchSnapshot(), POLL_MS)
    onCleanup(() => {
      ws?.close()
      if (pollTimer) clearInterval(pollTimer)
    })
  })

  // Derived data
  const agents     = () => Object.entries(snap.data?.agents ?? {})
  const tasks      = () => snap.data?.tasks ?? []
  const dagNodes   = () => snap.data?.dag?.nodes ?? []
  const dagEdges   = () => snap.data?.dag?.edges ?? []
  const busLog     = () => snap.data?.bus_log ?? []
  const agentNames = () => Object.keys(snap.data?.agents ?? {})
  const allAgents  = () => agentNames().length > 0
    ? agentNames()
    : ["planner", "builder", "debugger"]

  // Stats
  const aliveCount = createMemo(() =>
    agents().filter(([, i]) => i.alive || i.status === "idle" || i.status === "busy").length
  )
  const doneCount = createMemo(() => tasks().filter(t => t.status === "done").length)
  const failCount = createMemo(() => tasks().filter(t => t.status === "failed").length)

  // ── Agent actions ─────────────────────────────────────────────────────────

  const killAgent = async (name: string) => {
    await post(`/agents/${name}/kill`)
    void fetchSnapshot()
  }
  const pauseAgent = async (name: string, status: string) => {
    await post(`/agents/${name}/${status === "paused" ? "resume" : "pause"}`)
    void fetchSnapshot()
  }
  const spawnAgent = async (name: string, skills: string[]) => {
    setShowSpawn(false)
    await post("/agents/spawn", { name: name || undefined, skills })
    void fetchSnapshot()
  }
  const assignTask = async (agentName: string, desc: string) => {
    setAssignAgent(null)
    await post(`/agents/${agentName}/assign`, { description: desc })
    void fetchSnapshot()
  }

  return (
    <div style={{ padding: "8px 10px", "font-family": "inherit" }}>
      {/* Dialogs */}
      <Show when={showSpawn()}>
        <SpawnDialog
          onClose={() => setShowSpawn(false)}
          onSpawn={(n, s) => void spawnAgent(n, s)}
        />
      </Show>
      <Show when={assignAgent()}>
        <AssignDialog
          agentName={assignAgent()!}
          onClose={() => setAssignAgent(null)}
          onAssign={(d) => void assignTask(assignAgent()!, d)}
        />
      </Show>

      {/* Offline banner */}
      <Show when={snap.error && !snap.data}>
        <div style={{ ...card, color: "#f87171", "font-size": "12px", "text-align": "center" }}>
          ⚠ Swarm offline — {snap.error}
          <div style={{ "font-size": "10.5px", color: "#666", "margin-top": "4px" }}>
            Run <code style={{ background: "#2a2a2a", padding: "1px 4px", "border-radius": "3px" }}>
              cd swarm && .\start.ps1
            </code>
          </div>
        </div>
      </Show>

      <Show when={snap.loading && !snap.data}>
        <div style={{ "text-align": "center", color: "#555", "font-size": "12px", padding: "20px 0" }}>
          Connecting to swarm…
        </div>
      </Show>

      <Show when={snap.data}>
        {/* Header stats */}
        <div style={{ ...card, display: "flex", gap: "10px", "flex-wrap": "wrap", "align-items": "center", "margin-bottom": "8px" }}>
          <div style={{ display: "flex", gap: "6px", "align-items": "center" }}>
            <span style={{ width: "7px", height: "7px", "border-radius": "50%",
              background: snap.wsConnected ? "#4ade80" : "#facc15",
              display: "inline-block" }} />
            <span style={{ "font-size": "11px", color: "#888" }}>
              {snap.wsConnected ? "live" : "polling"}
            </span>
          </div>
          <span style={badge("#4ade80")}>{aliveCount()} agents up</span>
          <span style={badge("#60a5fa")}>{tasks().filter(t => t.status === "running" || t.status === "assigned").length} running</span>
          <span style={badge("#888")}>{doneCount()} done</span>
          <Show when={failCount() > 0}>
            <span style={badge("#f87171")}>{failCount()} failed</span>
          </Show>
          <div style={{ flex: "1" }} />
          <button onClick={() => setShowSpawn(true)} style={btn("#a78bfa")}>
            ⚡ Spawn Agent
          </button>
        </div>

        {/* Agents */}
        <Section title="Agents" default={true}>
          <For each={agents()}>
            {([name, info]) => (
              <AgentCard
                name={name}
                info={info}
                onKill={() => void killAgent(name)}
                onPause={() => void pauseAgent(name, info.status ?? "idle")}
                onAssign={() => setAssignAgent(name)}
              />
            )}
          </For>
        </Section>

        {/* DAG */}
        <Section title={`Task DAG (${dagNodes().length} nodes)`} default={false}>
          <div style={{ "padding-top": "6px" }}>
            <DAGView nodes={dagNodes()} edges={dagEdges()} />
          </div>
        </Section>

        {/* Recent Tasks */}
        <Section title={`Recent Tasks (${tasks().length})`} default={true}>
          <Show when={tasks().length === 0}>
            <div style={{ "font-size": "12px", color: "#444", padding: "8px 0" }}>No tasks yet</div>
          </Show>
          <For each={tasks().slice(0, 12)}>
            {(t) => <TaskRow task={t} />}
          </For>
        </Section>

        {/* Bus log */}
        <Section title="Agent Communication Log" default={false}>
          <div style={{ "padding-top": "4px" }}>
            <BusLog entries={busLog()} />
          </div>
        </Section>

        {/* Submit */}
        <Section title="New Task" default={true}>
          <div style={{ "padding-top": "4px" }}>
            <SubmitForm agents={allAgents()} />
          </div>
        </Section>
      </Show>
    </div>
  )
}
