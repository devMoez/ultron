import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  target: z
    .string()
    .describe(
      "What to open: an app name (e.g. 'notepad', 'chrome', 'vscode'), a file path, a folder path, or a URL (e.g. 'https://google.com')",
    ),
})

const DESCRIPTION = `Open an application, file, folder, or URL on the system.

Examples:
- Open an app by name: { "target": "notepad" }
- Open a URL: { "target": "https://github.com" }
- Open a folder: { "target": "C:\\Users\\user\\Documents" }
- Open a file: { "target": "C:\\path\\to\\file.pdf" }

On Windows, uses the 'start' command which resolves app names, file associations, and URLs automatically.`

export const OpenAppTool = Tool.define(
  "open_app",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, _ctx: Tool.Context) =>
      Effect.gen(function* () {
        const platform = os.platform()
        let command: string

        if (platform === "win32") {
          command = `cmd /c start "" "${params.target.replace(/"/g, '\\"')}"`
        } else if (platform === "darwin") {
          command = `open "${params.target.replace(/"/g, '\\"')}"`
        } else {
          command = `xdg-open "${params.target.replace(/"/g, '\\"')}"`
        }

        yield* Effect.tryPromise(() => execAsync(command)).pipe(Effect.orDie)
        return {
          title: `Opened: ${params.target}`,
          output: `✓ Successfully opened: ${params.target}`,
          metadata: { target: params.target, platform },
        }
      }),
  }),
)