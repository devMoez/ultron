/**
 * Cross-tab @mention parsing and resolution.
 *
 * Syntax:
 *   @chat[id_or_title]            – reference entire chat
 *   @chat[id]:message_index       – reference specific message
 *   @code[session_id]             – reference code session
 *   @cowork[task_id]              – reference cowork task
 *
 * Resolution: finds the session's recent messages from local storage map
 * and injects them as a read-only context block in the prompt text.
 */

export type CrossMentionType = "chat" | "code" | "cowork"

export type CrossMention = {
  type: CrossMentionType
  id: string
  messageIndex?: number
  raw: string // the raw @mention string to replace
}

const MENTION_RE = /@(chat|code|cowork)\[([^\]]+)\](?::(\d+))?/g

/** Parse all cross-mentions from prompt text. */
export function parseCrossMentions(text: string): CrossMention[] {
  const mentions: CrossMention[] = []
  let m: RegExpExecArray | null
  MENTION_RE.lastIndex = 0
  while ((m = MENTION_RE.exec(text)) !== null) {
    mentions.push({
      type: m[1] as CrossMentionType,
      id: m[2],
      messageIndex: m[3] !== undefined ? parseInt(m[3], 10) : undefined,
      raw: m[0],
    })
  }
  return mentions
}

export type SessionMessage = {
  id: string
  role: "user" | "assistant"
  text: string
}

/**
 * Resolve cross-mentions in `text`.
 * `getSessionMessages(id)` should return recent messages for a session ID.
 *
 * Returns the resolved text (mentions replaced with context blocks).
 */
export function resolveCrossMentions(
  text: string,
  getSessionMessages: (id: string) => SessionMessage[],
  getSessionTitle: (id: string) => string,
): string {
  const mentions = parseCrossMentions(text)
  if (mentions.length === 0) return text

  let resolved = text
  const seenRaw = new Set<string>()

  for (const mention of mentions) {
    if (seenRaw.has(mention.raw)) continue
    seenRaw.add(mention.raw)

    const messages = getSessionMessages(mention.id)
    if (messages.length === 0) continue

    const title = getSessionTitle(mention.id) || `${mention.type}/${mention.id}`
    let block: string

    if (mention.messageIndex !== undefined) {
      const msg = messages[mention.messageIndex]
      if (!msg) continue
      block = formatContextBlock(title, [msg], mention.type)
    } else {
      // Last 8 messages for context
      const recent = messages.slice(-8)
      block = formatContextBlock(title, recent, mention.type)
    }

    resolved = resolved.replace(mention.raw, block)
  }

  return resolved
}

function formatContextBlock(
  title: string,
  messages: SessionMessage[],
  type: CrossMentionType,
): string {
  const label = type === "chat" ? "Chat" : type === "code" ? "Code Session" : "Cowork Task"
  const lines = [
    `[Cross-reference: ${label} "${title}"]`,
    ...messages.map((m) => `${m.role === "user" ? "User" : "AI"}: ${m.text.slice(0, 400)}`),
    `[End cross-reference]`,
  ]
  return lines.join("\n")
}
