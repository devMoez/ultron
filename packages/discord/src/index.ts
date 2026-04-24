import { Client, GatewayIntentBits, Events, Message, ActivityType } from "discord.js"
import { createOpencodeClient } from "@opencode-ai/sdk"
import { EventEmitter } from "events"

const token = process.env.DISCORD_BOT_TOKEN
if (!token) throw new Error("DISCORD_BOT_TOKEN is required")

// Optional: restrict to specific guild/server IDs (comma-separated)
const allowedGuildIds = process.env.DISCORD_ALLOWED_GUILD_IDS
  ? process.env.DISCORD_ALLOWED_GUILD_IDS.split(",").map((id) => id.trim()).filter(Boolean)
  : []

// Optional: restrict to specific user IDs (comma-separated)
const allowedUserIds = process.env.DISCORD_ALLOWED_USER_IDS
  ? process.env.DISCORD_ALLOWED_USER_IDS.split(",").map((id) => id.trim()).filter(Boolean)
  : []

console.log("🔧 Bot configuration:")
console.log("- Bot token present:", !!token)
console.log("- Allowed guild IDs:", allowedGuildIds.length > 0 ? allowedGuildIds.join(", ") : "all")
console.log("- Allowed user IDs:", allowedUserIds.length > 0 ? allowedUserIds.join(", ") : "all")

// ─── Spawn ultron server ──────────────────────────────────────────────────────
console.log("🚀 Starting ultron server...")
const ultronBin = process.env.OPENCODE_BIN_PATH ?? "ultron"
const serverPort = Number(process.env.OPENCODE_PORT ?? 4096)
const serverUrl = `http://127.0.0.1:${serverPort}`

const proc = Bun.spawn([ultronBin, "serve", `--hostname=127.0.0.1`, `--port=${serverPort}`], {
  stdout: "pipe",
  stderr: "pipe",
  env: { ...process.env },
})

const deadline = Date.now() + 60_000
while (Date.now() < deadline) {
  try {
    const res = await fetch(`${serverUrl}/`)
    if (res.status < 500) break
  } catch {
    // not ready yet
  }
  await Bun.sleep(500)
}
if (Date.now() >= deadline) {
  proc.kill()
  throw new Error("Timeout: ultron server did not start within 60s")
}

const client_api = createOpencodeClient({ baseUrl: serverUrl })
console.log("✅ Ultron server ready at", serverUrl)

// ─── Shared SSE event bus ─────────────────────────────────────────────────────
const bus = new EventEmitter()
bus.setMaxListeners(100)

void (async () => {
  while (true) {
    try {
      const events = await client_api.event.subscribe()
      for await (const event of events.stream) {
        bus.emit("event", event)
      }
    } catch {
      await Bun.sleep(2000)
    }
  }
})()

// ─── Wait for AI response ─────────────────────────────────────────────────────
async function waitForResponse(sessionID: string, _unused: string | undefined, timeoutMs = 120_000): Promise<string> {
  return new Promise((resolve) => {
    // Collect parts keyed by partID → latest text
    const parts = new Map<string, string>()
    let seenBusy = false
    // First messageID we see belongs to the user — skip all its parts
    let userMessageID: string | null = null

    const timer = setTimeout(() => {
      bus.off("event", handler)
      const text = [...parts.values()].filter(Boolean).join("\n").trim()
      resolve(text || "⏱ Response timed out.")
    }, timeoutMs)

    function handler(event: any) {
      if (event.type === "session.status") {
        const { sessionID: sid, status } = event.properties
        if (sid !== sessionID) return
        if (status.type !== "idle") {
          seenBusy = true
          return
        }
        if (!seenBusy) return
        clearTimeout(timer)
        bus.off("event", handler)
        const text = [...parts.values()].filter(Boolean).join("\n").trim()
        resolve(text || "✅ Done.")
        return
      }

      if (event.type === "message.part.updated") {
        const part = event.properties.part
        if (part.sessionID !== sessionID) return
        if (part.type !== "text" || !part.text) return

        // First messageID = user's own message → skip it entirely
        if (!userMessageID) {
          userMessageID = part.messageID
          return
        }
        if (part.messageID === userMessageID) return

        // Everything else = assistant response
        parts.set(part.id, part.text)
      }
    }

    bus.on("event", handler)
  })
}

// ─── Strip ANSI/terminal escape codes ────────────────────────────────────────
function stripAnsi(text: string): string {
  // eslint-disable-next-line no-control-regex
  return text.replace(/\x1B\[[0-9;]*[a-zA-Z]/g, "")
             .replace(/\x1B\][^\x07]*\x07/g, "")
             .replace(/\x1B[@-Z\\-_]/g, "")
             .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, "")
             .trim()
}

// ─── Split long messages (Discord limit: 2000 chars) ─────────────────────────
function splitMessage(text: string, maxLen = 1900): string[] {
  if (text.length <= maxLen) return [text]
  const chunks: string[] = []
  let start = 0
  while (start < text.length) {
    // Try to break at newline
    let end = start + maxLen
    if (end < text.length) {
      const nl = text.lastIndexOf("\n", end)
      if (nl > start) end = nl + 1
    }
    chunks.push(text.slice(start, end))
    start = end
  }
  return chunks
}

// ─── Discord client ───────────────────────────────────────────────────────────
const discord = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.DirectMessages,
  ],
})

type Session = { sessionId: string; userId: string }
// Map keyed by userId (DM) or channelId (server) depending on context
const sessions = new Map<string, Session>()

function isAllowed(message: Message): boolean {
  if (allowedUserIds.length > 0 && !allowedUserIds.includes(message.author.id)) return false
  if (allowedGuildIds.length > 0 && message.guildId && !allowedGuildIds.includes(message.guildId)) return false
  return true
}

// Session key: per-user in DMs, per-channel in servers
function sessionKey(message: Message): string {
  return message.guildId ? message.channelId : message.author.id
}

discord.once(Events.ClientReady, (c) => {
  console.log(`⚡️ Discord bot ready! Logged in as ${c.user.tag}`)
  c.user.setActivity("Ultron", { type: ActivityType.Watching })
})

discord.on(Events.MessageCreate, async (message) => {
  // Ignore bots (including self)
  if (message.author.bot) return

  // Respond to everything in DMs, and everything in servers too
  const inDM = !message.guildId
  const mentioned = message.mentions.has(discord.user!)
  // In servers: respond to all messages (not just mentions)
  // Remove this check if you want server-wide responses, keep it for mention-only
  void inDM; void mentioned;

  if (!isAllowed(message)) {
    await message.reply("❌ Not authorized.")
    return
  }

  // Strip mention prefix from text
  let text = message.content.replace(/<@!?\d+>/g, "").trim()

  // Commands
  if (text === "!ping") {
    await message.reply("🏓 Pong! Ultron is online.")
    return
  }

  if (text === "!help" || text === "/help") {
    await message.reply(
      "**🤖 Ultron Bot**\n\n" +
      "Message me directly (DM) or mention me in a server.\n\n" +
      "**Commands:**\n" +
      "`!reset` — start a fresh session\n" +
      "`!status` — show session info\n" +
      "`!help` — this message\n\n" +
      "Just send any message and I'll handle it."
    )
    return
  }

  if (text === "!reset" || text === "/reset") {
    const key = sessionKey(message)
    sessions.delete(key)
    await message.reply("🔄 Session cleared. Next message starts fresh.")
    return
  }

  if (text === "!status" || text === "/status") {
    const key = sessionKey(message)
    const session = sessions.get(key)
    if (!session) {
      await message.reply("No active session. Send a message to start one.")
    } else {
      await message.reply(`✅ Session: \`${session.sessionId}\`\n🌐 Server: ${serverUrl}`)
    }
    return
  }

  if (!text) {
    await message.reply("Send me something to do!")
    return
  }

  const key = sessionKey(message)
  console.log(`📨 [${key}] ${text.substring(0, 80)}`)

  // Show typing indicator
  let typingStop = false
  const keepTyping = async () => {
    while (!typingStop) {
      await message.channel.sendTyping().catch(() => {})
      await Bun.sleep(8000)
    }
  }
  void keepTyping()

  try {
    let session = sessions.get(key)

    if (!session) {
      console.log("🆕 Creating session...")
      const createResult = await client_api.session.create({
        body: { title: `Discord ${key}` },
      })
      if (createResult.error) {
        typingStop = true
        console.error("❌ Session create error:", createResult.error)
        await message.reply("❌ Couldn't create a session. Is ultron running?")
        return
      }
      const sessionId = createResult.data.id
      console.log("✅ Session:", sessionId)
      session = { sessionId, userId: message.author.id }
      sessions.set(key, session)
    }

    const { sessionId } = session

    const promptResult = await client_api.session.promptAsync({
      path: { id: sessionId },
      body: { parts: [{ type: "text", text }] },
    })
    if (promptResult.error) {
      typingStop = true
      console.error("❌ Prompt error:", promptResult.error)
      await message.reply("❌ Failed to send your message. Try `!reset` and resend.")
      return
    }

    // The user message ID — filter its parts out so we don't echo the input back
    const userMessageID = (promptResult.data as any)?.id as string | undefined

    console.log("⏳ Waiting for response...")
    const response = await waitForResponse(sessionId, userMessageID)
    typingStop = true

    const clean = stripAnsi(response)
    console.log("💬 Response:", clean.substring(0, 80))
    const chunks = splitMessage(clean)
    for (const chunk of chunks) {
      await message.reply(chunk)
    }
  } catch (err) {
    typingStop = true
    console.error("💥 Error:", err)
    await message.reply("❌ Something went wrong. Try again or `!reset`.")
  }
})

process.on("SIGINT", () => {
  proc.kill()
  process.exit(0)
})

await discord.login(token)
