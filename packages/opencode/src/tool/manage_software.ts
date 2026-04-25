import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  action: z
    .enum(["install", "uninstall", "list", "search", "upgrade", "info"])
    .describe(
      "Action: install a package, uninstall it, list installed apps, search available packages, upgrade a package, or get info about a package.",
    ),
  package: z
    .string()
    .optional()
    .describe(
      "Package name or ID. Required for install, uninstall, upgrade, info. For install/search you can use a friendly name like 'vlc', 'vscode', 'git', '7zip'.",
    ),
  silent: z
    .boolean()
    .optional()
    .default(true)
    .describe("Install silently without GUI prompts. Default true."),
})

const DESCRIPTION = `Install, uninstall, list, search, upgrade, or get info about software on Windows using winget.

Examples:
- Install VLC: { "action": "install", "package": "VLC.VLC" }
- Install Git: { "action": "install", "package": "Git.Git" }
- Install VSCode: { "action": "install", "package": "Microsoft.VisualStudioCode" }
- Uninstall: { "action": "uninstall", "package": "VLC.VLC" }
- Search for a package: { "action": "search", "package": "notepad" }
- List installed apps: { "action": "list" }
- Upgrade a package: { "action": "upgrade", "package": "Git.Git" }
- Package info: { "action": "info", "package": "Microsoft.VisualStudioCode" }

Common package IDs:
- git: Git.Git
- nodejs: OpenJS.NodeJS
- python: Python.Python.3.12
- vscode: Microsoft.VisualStudioCode
- chrome: Google.Chrome
- firefox: Mozilla.Firefox
- vlc: VideoLAN.VLC
- 7zip: 7zip.7zip
- notepad++: Notepad++.Notepad++
- discord: Discord.Discord
- spotify: Spotify.Spotify
- steam: Valve.Steam
- obs: OBSProject.OBSStudio`

export const ManageSoftwareTool = Tool.define(
  "manage_software",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, ctx: Tool.Context) =>
      Effect.gen(function* () {
        const platform = os.platform()

        if (platform !== "win32") {
          return {
            title: "manage_software: Windows only",
            output: "This tool uses winget and is only available on Windows. On Linux, use the bash tool with apt/pacman/etc. On macOS, use homebrew via the bash tool.",
            metadata: { action: params.action, package: params.package ?? "" },
          }
        }

        if (params.action === "install" || params.action === "uninstall" || params.action === "upgrade") {
          yield* ctx.ask({
            permission: "bash",
            patterns: [`manage_software:${params.action}:${params.package}`],
            always: [],
            metadata: {
              action: params.action,
              package: params.package,
              description: `${params.action} "${params.package}" via winget`,
            },
          })
        }

        const pkg = params.package ?? ""
        let command: string

        switch (params.action) {
          case "install":
            if (!pkg) throw new Error("Package name required for install")
            command = `winget install --id "${pkg}"${params.silent ? " --silent" : ""} --accept-package-agreements --accept-source-agreements`
            break
          case "uninstall":
            if (!pkg) throw new Error("Package name required for uninstall")
            command = `winget uninstall --id "${pkg}"${params.silent ? " --silent" : ""}`
            break
          case "list":
            command = "winget list"
            break
          case "search":
            if (!pkg) throw new Error("Search term required")
            command = `winget search "${pkg}"`
            break
          case "upgrade":
            if (!pkg) throw new Error("Package name required for upgrade")
            command = `winget upgrade --id "${pkg}"${params.silent ? " --silent" : ""} --accept-package-agreements --accept-source-agreements`
            break
          case "info":
            if (!pkg) throw new Error("Package name required for info")
            command = `winget show --id "${pkg}"`
            break
          default:
            throw new Error(`Unknown action: ${params.action}`)
        }

        const { stdout, stderr } = yield* Effect.tryPromise(() => execAsync(command, { timeout: 120000 })).pipe(Effect.orDie)
        const output = (stdout + (stderr ? `\nSTDERR: ${stderr}` : "")).trim()
        return {
          title: `${params.action}${pkg ? `: ${pkg}` : ""}`,
          output: output || `✓ ${params.action} completed successfully.`,
          metadata: { action: params.action, package: pkg },
        }
      }),
  }),
)