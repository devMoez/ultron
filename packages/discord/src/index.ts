import { Client, GatewayIntentBits, Events, Message, ActivityType } from "discord.js"
import { createOpencodeClient } from "@opencode-ai/sdk"
import { EventEmitter } from "events"
import { spawn, ChildProcess } from "child_process"

// ─── Utility: Node.js sleep ─────────────────────────────────────────────────────
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

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
const ultronBin = process.env.OPENCODE_BIN_PATH ?? "node"
const opencodeDir = process.env.OPENCODE_DIR ?? "C:/Users/moezf/Desktop/opencode/packages/opencode"
const serverPort = Number(process.env.OPENCODE_PORT ?? 4096)
const serverUrl = `http://127.0.0.1:${serverPort}`

// Use node to run the server (not bun)
const serverArgs = ultronBin === "node" 
  ? ["./bin/opencode.cjs", "serve", `--hostname=127.0.0.1`, `--port=${serverPort}`]
  : [ultronBin, "serve", `--hostname=127.0.0.1`, `--port=${serverPort}`]

const proc: ChildProcess = spawn(ultronBin === "node" ? "node" : ultronBin, serverArgs, {
  cwd: opencodeDir,
  stdio: ["ignore", "pipe", "pipe"],
  env: { ...process.env },
  shell: true,
})

proc.stdout?.on("data", (data) => console.log(`[server] ${data}`))
proc.stderr?.on("data", (data) => console.error(`[server] ${data}`))

// Wait for server to be ready
const deadline = Date.now() + 60_000
while (Date.now() < deadline) {
  try {
    const res = await fetch(`${serverUrl}/`)
    if (res.status < 500) break
  } catch {
    // not ready yet
  }
  await sleep(500)
}
if (Date.now() >= deadline) {
  proc.kill()
  throw new Error("Timeout: ultron server did not start within 60s")
}

const client_api = createOpencodeClient({ baseUrl: serverUrl })
console.log("✅ Ultron server ready at", serverUrl)

// ─── Helper: check if process is alive ───────────────────────────────────────
function isProcAlive(): boolean {
  return proc && !proc.killed && proc.pid !== undefined
}

// ─── Helper: restart server ───────────────────────────────────────────────────
async function restartServer(): Promise<boolean> {
  console.log("🔄 Restarting server...")
  
  // Kill existing process
  if (isProcAlive()) {
    proc.kill("SIGTERM")
    await sleep(1000)
  }
  
  // Spawn new process
  const newProc = spawn(ultronBin === "node" ? "node" : ultronBin, serverArgs, {
    cwd: opencodeDir,
    stdio: ["ignore", "pipe", "pipe"],
    env: { ...process.env },
    shell: true,
  })
  
  // Copy to global proc
  Object.assign(proc, newProc)
  
  // Wait for ready
  const restartDeadline = Date.now() + 60_000
  while (Date.now() < restartDeadline) {
    try {
      const res = await fetch(`${serverUrl}/`)
      if (res.status < 500) return true
    } catch {
      // not ready
    }
    await sleep(500)
  }
  
  return false
}

// ─── Shared SSE event bus ─────────────────────────────────────────────────────
const bus = new EventEmitter()
bus.setMaxListeners(100)

void (async () => {
  while (true) {
    try {
      console.log("🔌 Connecting to SSE event stream...")
      const events = await client_api.event.subscribe()
      console.log("✅ SSE connected")
      for await (const event of events.stream) {
        const e = event as any
        if (e.type?.startsWith("session.") || e.type?.startsWith("message.")) {
          console.log(`📡 SSE: ${e.type} | ${JSON.stringify(e.properties ?? {}).substring(0, 120)}`)
        }
        bus.emit("event", event)
      }
    } catch (err) {
      console.error("❌ SSE disconnected:", err)
      await sleep(2000)
    }
  }
})()

// ─── Fetch last assistant message from session ────────────────────────────────
async function fetchLastAssistantMessage(sessionID: string): Promise<string | null> {
  const result = await client_api.session.messages({ path: { id: sessionID } })
  // API returns UIMessage[]: { id, role, parts } — no "info" wrapper
  const messages = (result.data ?? []) as Array<{
    id: string
    role: string
    parts: Array<{ type: string; text?: string }>
  }>
  console.log(`📬 ${messages.length} messages: ${messages.map(m => m.role).join(",")}`)
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i]
    if (msg.role !== "assistant") continue
    const text = (msg.parts ?? [])
      .filter(p => p.type === "text" && p.text)
      .map(p => p.text!)
      .join("\n").trim()
    if (text) return text
  }
  return null
}

// ─── Wait for AI response ─────────────────────────────────────────────────────
async function waitForResponse(sessionID: string, _unused?: string, timeoutMs = 120_000): Promise<string> {
  // Wait for session to go busy → idle via SSE
  let seenBusy = false
  let resolved = false

  await new Promise<void>((resolve) => {
    const timer = setTimeout(() => {
      console.log("⏰ SSE timeout — proceeding to fetch anyway")
      bus.off("event", handler)
      resolve()
    }, timeoutMs)

    function done() {
      if (resolved) return
      resolved = true
      clearTimeout(timer)
      bus.off("event", handler)
      resolve()
    }

    function handler(event: any) {
      const props = event.properties ?? {}
      const sid = props.sessionID ?? props.session_id

      // session.idle is the legacy event — always means done
      if (event.type === "session.idle") {
        if (sid !== sessionID) return
        console.log(`📡 session.idle for ${sid}`)
        seenBusy = true  // treat idle as having seen busy
        done()
        return
      }

      if (event.type !== "session.status") return
      if (sid !== sessionID) return
      const statusType = props.status?.type ?? props.type
      console.log(`📡 session.status for ${sid}: ${statusType}`)

      if (statusType === "busy" || statusType === "retry") {
        seenBusy = true
        return
      }
      if (statusType === "idle" && seenBusy) {
        done()
      }
    }
    bus.on("event", handler)
  })

  // Poll for assistant message — retry a few times in case of DB lag
  for (let i = 0; i < 6; i++) {
    await sleep(500)
    const text = await fetchLastAssistantMessage(sessionID).catch(() => null)
    if (text) return text
    console.log(`⏳ Poll ${i + 1}: no assistant text yet`)
  }

  return ""
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
      "`/ultron` — start/restart server\n" +
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

  // ─── /ultron command — start/restart server ─────────────────────────────────
  if (text === "/ultron") {
    await message.reply("🔄 Starting Ultron server...")
    
    const success = await restartServer()
    
    if (success) {
      await message.reply(`✅ Ultron server started!\n🌐 ${serverUrl}`)
    } else {
      await message.reply("❌ Server failed to start within 60s")
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
      await sleep(8000)
    }
  }
  void keepTyping()

  try {
    let session = sessions.get(key)

    const workDir = process.cwd()

    if (!session) {
      console.log("🆕 Creating session...")
      const createResult = await client_api.session.create({
        body: { title: `Discord ${key}` },
        query: { directory: workDir },
      })
      if (createResult.error) {
        typingStop = true
        console.error("❌ Session create error:", createResult.error)
        await message.reply("❌ Couldn't create a session.")
        return
      }
      const sessionId = createResult.data.id
      console.log("✅ Session:", sessionId)
      session = { sessionId, userId: message.author.id }
      sessions.set(key, session)
    }

    const { sessionId } = session

    console.log("⏳ Sending prompt...")
    const promptResult = await client_api.session.promptAsync({
      path: { id: sessionId },
      body: { parts: [{ type: "text", text }] },
      query: { directory: workDir },
    })

    if (promptResult.error) {
      typingStop = true
      console.error("❌ Prompt error:", promptResult.error)
      await message.reply("❌ Failed to send message. Try `!reset`.")
      return
    }

    console.log("⏳ Waiting for AI response...")
    const responseText = await waitForResponse(sessionId)
    typingStop = true

    console.log(`💬 Response (${responseText.length} chars): ${responseText.substring(0, 100)}`)

    if (!responseText) {
      await message.reply("⏱ No response received.")
      return
    }

    const clean = stripAnsi(responseText)
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
  if (isProcAlive()) {
    proc.kill("SIGTERM")
  }
  process.exit(0)
})

await discord.login(token)