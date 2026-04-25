import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  query: z.string().describe("File name or pattern to search for. Supports wildcards: e.g. '*.pdf', 'report*', 'config.json'"),
  searchIn: z
    .string()
    .optional()
    .describe(
      "Directory to search in. Defaults to the user's home directory. Use 'C:\\' to search the entire C drive (slower).",
    ),
  type: z
    .enum(["any", "file", "folder"])
    .default("any")
    .describe("Search for files, folders, or both."),
  maxResults: z
    .number()
    .optional()
    .default(20)
    .describe("Maximum number of results to return. Default 20."),
})

const DESCRIPTION = `Search for files and folders on the system by name or pattern.

Examples:
- Find all PDFs: { "query": "*.pdf" }
- Find a specific file: { "query": "resume.docx" }
- Find files matching a pattern: { "query": "report*", "searchIn": "C:\\Users\\user\\Documents" }
- Find a folder: { "query": "node_modules", "type": "folder" }
- Search the whole C drive: { "query": "config.json", "searchIn": "C:\\" }

Returns full paths to matching files/folders. Searches are limited to avoid timeouts.`

export const SearchSystemTool = Tool.define(
  "search_system",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, _ctx: Tool.Context) =>
      Effect.gen(function* () {
        const platform = os.platform()
        const searchRoot = params.searchIn ?? os.homedir()
        const maxResults = params.maxResults ?? 20

        let results: string[] = []

        if (platform === "win32") {
          const typeFilter =
            params.type === "file"
              ? "-File"
              : params.type === "folder"
                ? "-Directory"
                : ""

          const ps = `
$results = Get-ChildItem -Path "${searchRoot.replace(/"/g, '`"')}" ` +
            `-Filter "${params.query.replace(/"/g, '`"')}" ` +
            `-Recurse -ErrorAction SilentlyContinue ${typeFilter} ` +
            `| Select-Object -First ${maxResults} -ExpandProperty FullName
$results
`.trim()

          const { stdout } = yield* Effect.tryPromise(() =>
            execAsync(`powershell -NoProfile -Command "${ps.replace(/\n/g, " ").replace(/"/g, '\\"')}"`, {
              timeout: 30000,
            }),
          ).pipe(Effect.orDie)

          results = stdout
            .split("\n")
            .map((l) => l.trim())
            .filter(Boolean)
        } else {
          const typeFlag = params.type === "file" ? "-type f" : params.type === "folder" ? "-type d" : ""
          const { stdout } = yield* Effect.tryPromise(() =>
            execAsync(
              `find "${searchRoot}" -name "${params.query}" ${typeFlag} 2>/dev/null | head -${maxResults}`,
              { timeout: 30000 },
            ),
          ).pipe(Effect.orDie)
          results = stdout
            .split("\n")
            .map((l) => l.trim())
            .filter(Boolean)
        }

        if (results.length === 0) {
          return {
            title: `No results for: ${params.query}`,
            output: `No files or folders matching "${params.query}" found in "${searchRoot}".\n\nTry:\n- A different search pattern (e.g. use wildcards: *.pdf)\n- A different directory (e.g. "C:\\" to search the whole drive)\n- Checking spelling`,
            metadata: { query: params.query, searchIn: searchRoot, count: 0, results: [] as string[] },
          }
        }

        const output = [
          `Found ${results.length} result${results.length !== 1 ? "s" : ""} for "${params.query}" in "${searchRoot}":`,
          "",
          ...results.map((r, i) => `${(i + 1).toString().padStart(2)}. ${r}`),
          results.length >= maxResults ? `\n(Showing first ${maxResults} results. Narrow your search or increase maxResults for more.)` : "",
        ]
          .join("\n")
          .trim()

        return {
          title: `Found ${results.length} result(s) for: ${params.query}`,
          output,
          metadata: { query: params.query, searchIn: searchRoot, count: results.length, results },
        }
      }),
  }),
)