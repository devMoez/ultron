/**
 * Ultron Pinned Store
 * Persists pinned messages (per session) and pinned entities (global) to localStorage.
 * Reactive — updates propagate to all consumers immediately.
 */
import { createContext, useContext, type JSX } from "solid-js"
import { createStore } from "solid-js/store"
import type { TabType } from "./session-type"

const MSG_KEY = "ultron:pinned-messages"
const ENT_KEY = "ultron:pinned-entities"

export type PinnedMessage = {
  messageId: string
  text: string // first ~200 chars of text content
  role: "user" | "assistant"
  pinnedAt: number
}

export type PinnedEntity = {
  type: TabType
  id: string
  title: string
  pinnedAt: number
}

type PinnedStore = {
  // Messages pinned per session
  messages: Record<string, PinnedMessage[]>
  // Entities pinned globally (chats / sessions / cowork tasks)
  entities: PinnedEntity[]
}

type PinnedActions = {
  pinMessage(sessionId: string, msg: Omit<PinnedMessage, "pinnedAt">): void
  unpinMessage(sessionId: string, messageId: string): void
  isPinnedMessage(sessionId: string, messageId: string): boolean
  pinnedMessages(sessionId: string): PinnedMessage[]

  pinEntity(entity: Omit<PinnedEntity, "pinnedAt">): void
  unpinEntity(id: string): void
  isPinnedEntity(id: string): boolean
  pinnedEntities(): PinnedEntity[]
}

function loadMsgs(): Record<string, PinnedMessage[]> {
  try { return JSON.parse(localStorage.getItem(MSG_KEY) ?? "{}") as Record<string, PinnedMessage[]> } catch { return {} }
}
function loadEnts(): PinnedEntity[] {
  try { return JSON.parse(localStorage.getItem(ENT_KEY) ?? "[]") as PinnedEntity[] } catch { return [] }
}
function saveMsgs(v: Record<string, PinnedMessage[]>) {
  try { localStorage.setItem(MSG_KEY, JSON.stringify(v)) } catch {}
}
function saveEnts(v: PinnedEntity[]) {
  try { localStorage.setItem(ENT_KEY, JSON.stringify(v)) } catch {}
}

const Ctx = createContext<PinnedActions>()

export function PinnedStoreProvider(props: { children: JSX.Element }) {
  const [store, setStore] = createStore<PinnedStore>({
    messages: loadMsgs(),
    entities: loadEnts(),
  })

  const actions: PinnedActions = {
    pinMessage(sessionId, msg) {
      const existing = store.messages[sessionId] ?? []
      if (existing.some((m) => m.messageId === msg.messageId)) return
      const next = [...existing, { ...msg, pinnedAt: Date.now() }]
      setStore("messages", sessionId, next)
      saveMsgs({ ...store.messages, [sessionId]: next })
    },
    unpinMessage(sessionId, messageId) {
      const next = (store.messages[sessionId] ?? []).filter((m) => m.messageId !== messageId)
      setStore("messages", sessionId, next)
      saveMsgs({ ...store.messages, [sessionId]: next })
    },
    isPinnedMessage(sessionId, messageId) {
      return (store.messages[sessionId] ?? []).some((m) => m.messageId === messageId)
    },
    pinnedMessages(sessionId) {
      return store.messages[sessionId] ?? []
    },

    pinEntity(entity) {
      if (store.entities.some((e) => e.id === entity.id)) return
      const next = [...store.entities, { ...entity, pinnedAt: Date.now() }]
      setStore("entities", next)
      saveEnts(next)
    },
    unpinEntity(id) {
      const next = store.entities.filter((e) => e.id !== id)
      setStore("entities", next)
      saveEnts(next)
    },
    isPinnedEntity(id) {
      return store.entities.some((e) => e.id === id)
    },
    pinnedEntities() {
      return store.entities
    },
  }

  return <Ctx.Provider value={actions}>{props.children}</Ctx.Provider>
}

export function usePinnedStore(): PinnedActions {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error("usePinnedStore must be used within PinnedStoreProvider")
  return ctx
}
