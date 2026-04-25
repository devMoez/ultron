import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  action: z
    .enum(["shutdown", "restart", "sleep", "hibernate", "lock", "logout", "cancel"])
    .describe(
      "Power action: shutdown, restart, sleep, hibernate, lock (lock screen), logout (sign out), or cancel (cancel a pending shutdown/restart)",
    ),
  delayMinutes: z
    .number()
    .optional()
    .default(0)
    .describe("Delay before action in minutes. 0 = immediate. Only applies to shutdown and restart."),
  force: z
    .boolean()
    .optional()
    .default(false)
    .describe("Force close apps without saving. Use with caution. Only applies to shutdown and restart."),
})

const DESCRIPTION = `Control system power state: shutdown, restart, sleep, hibernate, lock screen, logout, or cancel a pending shutdown.

Examples:
- Lock screen now: { "action": "lock" }
- Shutdown immediately: { "action": "shutdown" }
- Restart in 5 minutes: { "action": "restart", "delayMinutes": 5 }
- Sleep: { "action": "sleep" }
- Cancel pending shutdown: { "action": "cancel" }

⚠️ Shutdown, restart, hibernate, and logout are irreversible. Always confirm with the user before executing.`

function runAction(params: z.infer<typeof Parameters>) {
  return Effect.tryPromise(async () => {
    const platform = os.platform()
    const delaySec = (params.delayMinutes ?? 0) * 60
    const force = params.force ?? false

    if (platform === "win32") {
      let command: string
      switch (params.action) {
        case "shutdown":
          command = `shutdown /s /t ${delaySec}${force ? " /f" : ""}`
          break
        case "restart":
          command = `shutdown /r /t ${delaySec}${force ? " /f" : ""}`
          break
        case "sleep":
          command = "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
          break
        case "hibernate":
          command = "shutdown /h"
          break
        case "lock":
          command = "rundll32.exe user32.dll,LockWorkStation"
          break
        case "logout":
          command = "shutdown /l"
          break
        case "cancel":
          command = "shutdown /a"
          break
        default:
          throw new Error(`Unknown action: ${params.action}`)
      }
      await execAsync(command)
    } else if (platform === "darwin") {
      const cmds: Record<string, string> = {
        shutdown: `osascript -e 'tell app "System Events" to shut down'`,
        restart: `osascript -e 'tell app "System Events" to restart'`,
        sleep: `osascript -e 'tell app "System Events" to sleep'`,
        lock: `/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend`,
        logout: `osascript -e 'tell app "System Events" to log out'`,
        hibernate: `pmset sleepnow`,
        cancel: `killall -SIGTERM shutdown`,
      }
      await execAsync(cmds[params.action] ?? `echo "unsupported on macOS"`)
    } else {
      const cmds: Record<string, string> = {
        shutdown: `systemctl poweroff`,
        restart: `systemctl reboot`,
        sleep: `systemctl suspend`,
        hibernate: `systemctl hibernate`,
        lock: `loginctl lock-session`,
        logout: `loginctl terminate-session self`,
        cancel: `shutdown -c`,
      }
      await execAsync(cmds[params.action] ?? `echo "unsupported"`)
    }

    const messages: Record<string, string> = {
      shutdown: delaySec > 0 ? `Computer will shut down in ${params.delayMinutes} minute(s).` : "Shutting down...",
      restart: delaySec > 0 ? `Computer will restart in ${params.delayMinutes} minute(s).` : "Restarting...",
      sleep: "Going to sleep...",
      hibernate: "Hibernating...",
      lock: "Screen locked.",
      logout: "Logging out...",
      cancel: "Pending shutdown/restart cancelled.",
    }

    return {
      title: params.action.charAt(0).toUpperCase() + params.action.slice(1),
      output: `✓ ${messages[params.action] ?? params.action}`,
      metadata: { action: params.action, delaySec, force },
    }
  })
}

export const SystemPowerTool = Tool.define(
  "system_power",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, ctx: Tool.Context) => {
      if (params.action !== "lock" && params.action !== "cancel") {
        return Effect.flatMap(
          ctx.ask({
            permission: "bash",
            patterns: [`system_power:${params.action}`],
            always: [],
            metadata: {
              action: params.action,
              description: `Are you sure you want to ${params.action} the computer?`,
            },
          }),
          () => runAction(params),
        )
      }

      return runAction(params)
    },
  }),
)