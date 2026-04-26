import { Flag } from "@/flag/flag"
import { Hono } from "hono"
import { getMimeType } from "hono/utils/mime"
import fs from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

const embeddedUIPromise = Flag.OPENCODE_DISABLE_EMBEDDED_WEB_UI
  ? Promise.resolve(null)
  : // @ts-expect-error - generated file at build time
    import("opencode-web-ui.gen.ts").then((module) => module.default as Record<string, string>).catch(() => null)

// packages/app/dist – populated after `bun run build` in packages/app
const localDistDir = (() => {
  try {
    const here = fileURLToPath(import.meta.url)
    return path.resolve(path.dirname(here), "../../../../app/dist")
  } catch {
    return null
  }
})()

const DEFAULT_CSP =
  "default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; media-src 'self' data:; connect-src 'self' data:"

const NOT_BUILT_HTML = `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body{background:#1c1c1c;color:#e8e8e8;font-family:monospace;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}
.box{text-align:center;max-width:420px}
h2{color:#a78bfa;margin-bottom:12px}
code{background:#252525;border:1px solid #333;padding:6px 14px;border-radius:6px;display:block;margin:12px 0;color:#7dd3fc}
p{color:#888;font-size:13px}
</style></head><body><div class="box">
<h2>Ultron UI not built</h2>
<p>Run this once to build the web interface:</p>
<code>cd packages/app &amp;&amp; bun run build</code>
<p>Then restart Ultron.</p>
</div></body></html>`

export const UIRoutes = (): Hono =>
  new Hono().all("/*", async (c) => {
    const embeddedWebUI = await embeddedUIPromise
    const reqPath = c.req.path

    // 1. Embedded binary (compiled release)
    if (embeddedWebUI) {
      const match = embeddedWebUI[reqPath.replace(/^\//, "")] ?? embeddedWebUI["index.html"] ?? null
      if (!match) return c.json({ error: "Not Found" }, 404)
      if (await fs.exists(match)) {
        const mime = getMimeType(match) ?? "text/plain"
        c.header("Content-Type", mime)
        if (mime.startsWith("text/html")) c.header("Content-Security-Policy", DEFAULT_CSP)
        return c.body(new Uint8Array(await fs.readFile(match)))
      }
      return c.json({ error: "Not Found" }, 404)
    }

    // 2. Local build (packages/app/dist) – custom Ultron UI
    if (localDistDir) {
      const hasDistIndex = await fs
        .access(path.join(localDistDir, "index.html"))
        .then(() => true)
        .catch(() => false)

      if (hasDistIndex) {
        const rel = reqPath.replace(/^\//, "") || "index.html"
        const filePath = path.join(localDistDir, rel)
        const exists = await fs.access(filePath).then(() => true).catch(() => false)
        const target = exists ? filePath : path.join(localDistDir, "index.html")
        const mime = getMimeType(target) ?? "text/html"
        c.header("Content-Type", mime)
        if (mime.startsWith("text/html")) c.header("Content-Security-Policy", DEFAULT_CSP)
        return c.body(new Uint8Array(await fs.readFile(target)))
      }
    }

    // 3. Not built yet – show instructions instead of proxying to app.opencode.ai
    c.header("Content-Type", "text/html")
    return c.html(NOT_BUILT_HTML)
  })
