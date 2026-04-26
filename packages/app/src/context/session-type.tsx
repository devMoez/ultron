import { createContext, useContext, type JSX } from "solid-js"
import { createStore } from "solid-js/store"

export type TabType = "chat" | "code" | "cowork"

const STORAGE_KEY = "ultron:session-types"
const PENDING_KEY = "ultron:pending-session-type"

function loadMap(): Record<string, TabType> {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "{}") as Record<string, TabType>
  } catch {
    return {}
  }
}

function saveMap(map: Record<string, TabType>) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(map))
  } catch {}
}

type SessionTypeStore = {
  get(sessionId: string): TabType
  set(sessionId: string, type: TabType): void
  // Call before navigating to a new session — consumed on first session create
  setPending(type: TabType): void
  consumePending(): TabType
}

const Ctx = createContext<SessionTypeStore>()

export function SessionTypeProvider(props: { children: JSX.Element }) {
  const [map, setMap] = createStore<Record<string, TabType>>(loadMap())

  const store: SessionTypeStore = {
    get(id) {
      return map[id] ?? "code"
    },
    set(id, type) {
      setMap(id, type)
      saveMap({ ...map, [id]: type })
    },
    setPending(type) {
      try { sessionStorage.setItem(PENDING_KEY, type) } catch {}
    },
    consumePending(): TabType {
      try {
        const v = sessionStorage.getItem(PENDING_KEY) as TabType | null
        sessionStorage.removeItem(PENDING_KEY)
        return v ?? "code"
      } catch {
        return "code"
      }
    },
  }

  return <Ctx.Provider value={store}>{props.children}</Ctx.Provider>
}

export function useSessionType(): SessionTypeStore {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error("useSessionType must be used within SessionTypeProvider")
  return ctx
}
