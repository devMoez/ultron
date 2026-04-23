import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  title: z.string().describe("Notification title, shown in bold. E.g. 'Ultron' or 'Task Complete'"),
  message: z.string().describe("Notification body message. E.g. 'Your download finished!'"),
  sound: z
    .boolean()
    .optional()
    .default(false)
    .describe("Play a sound with the notification. Default false."),
})

const DESCRIPTION = `Send a desktop notification (Windows toast, macOS alert, or Linux notify-send).

Use this to:
- Alert the user when a long task completes
- Remind the user of something
- Notify about important events

Examples:
- Simple notification: { "title": "Ultron", "message": "Your task is done!" }
- With sound: { "title": "Reminder", "message": "Meeting in 5 minutes", "sound": true }`

export const SendNotificationTool = Tool.define(
  "send_notification",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, _ctx: Tool.Context) =>
      Effect.tryPromise(async () => {
        const platform = os.platform()

        if (platform === "win32") {
          // Use PowerShell Windows Toast notification
          const title = params.title.replace(/'/g, "''")
          const message = params.message.replace(/'/g, "''")
          const ps = `
Add-Type -AssemblyName System.Windows.Forms
$notify = New-Object System.Windows.Forms.NotifyIcon
$notify.Icon = [System.Drawing.SystemIcons]::Information
$notify.BalloonTipTitle = '${title}'
$notify.BalloonTipText = '${message}'
$notify.BalloonTipIcon = 'Info'
$notify.Visible = $true
$notify.ShowBalloonTip(5000)
Start-Sleep -Milliseconds 5100
$notify.Dispose()
`.trim()

          await execAsync(`powershell -NoProfile -WindowStyle Hidden -Command "${ps.replace(/\n/g, " ")}"`, {
            timeout: 10000,
          })
        } else if (platform === "darwin") {
          const title = params.title.replace(/"/g, '\\"')
          const message = params.message.replace(/"/g, '\\"')
          await execAsync(`osascript -e 'display notification "${message}" with title "${title}"'`)
        } else {
          // Linux: notify-send
          const title = params.title.replace(/"/g, '\\"')
          const message = params.message.replace(/"/g, '\\"')
          await execAsync(`notify-send "${title}" "${message}"`)
        }

        return {
          title: `Notification sent: ${params.title}`,
          output: `✓ Notification sent: "${params.title}" — ${params.message}`,
          metadata: { title: params.title, message: params.message },
        }
      }),
  }),
)
