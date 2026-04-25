#!/usr/bin/env bun
// Ultron Server Starter - opens UI in browser automatically
// Usage: bun run start.ts   or   ultron web

const PORT = process.env.OPENCODE_PORT ?? "4096"

console.log(`\n🔧 Ultron Server\n━━━━━━━━━━━━━━━━\n🌐 Starting on http://127.0.0.1:${PORT}\n`)

// Start the server
const proc = Bun.spawn(["ultron", "serve", "--hostname=127.0.0.1", `--port=${PORT}`], {
  stdout: "pipe",
  stderr: "pipe",
})

// Wait for server to be ready
const deadline = Date.now() + 30_000
while (Date.now() < deadline) {
  try {
    const res = await fetch(`http://127.0.0.1:${PORT}/`)
    if (res.ok) break
  } catch {
    // not ready yet
  }
  await Bun.sleep(500)
}

if (Date.now() >= deadline) {
  console.error("❌ Server failed to start")
  proc.kill()
  process.exit(1)
}

// Open browser using PowerShell on Windows
const isWindows = process.platform === "win32"
if (isWindows) {
  Bun.spawn(["powershell", "-Command", `Start-Process chrome -ArgumentList 'http://127.0.0.1:${PORT}'`])
} else {
  // macOS
  Bun.spawn(["open", `http://127.0.0.1:${PORT}`])
}

console.log("✅ Ultron ready!")