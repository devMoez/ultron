import z from "zod"
import { Effect } from "effect"
import { HttpClient } from "effect/unstable/http"
import * as Tool from "./tool"
import * as McpExa from "./mcp-exa"
import DESCRIPTION from "./websearch.txt"

// Tavily API key rotation — picks keys from TAVILY_API_KEYS env (comma-separated) or TAVILY_API_KEY
const _tavilyKeys: string[] = (() => {
  const multi = process.env.TAVILY_API_KEYS
  if (multi) return multi.split(",").map((k) => k.trim()).filter(Boolean)
  const single = process.env.TAVILY_API_KEY
  return single ? [single] : []
})()
let _tavilyKeyIndex = 0
function nextTavilyKey(): string | undefined {
  if (_tavilyKeys.length === 0) return undefined
  const key = _tavilyKeys[_tavilyKeyIndex % _tavilyKeys.length]
  _tavilyKeyIndex++
  return key
}

const Parameters = z.object({
  query: z.string().describe("Websearch query"),
  numResults: z.number().optional().describe("Number of search results to return (default: 8)"),
  livecrawl: z
    .enum(["fallback", "preferred"])
    .optional()
    .describe(
      "Live crawl mode - 'fallback': use live crawling as backup if cached content unavailable, 'preferred': prioritize live crawling (default: 'fallback')",
    ),
  type: z
    .enum(["auto", "fast", "deep"])
    .optional()
    .describe("Search type - 'auto': balanced search (default), 'fast': quick results, 'deep': comprehensive search"),
  contextMaxCharacters: z
    .number()
    .optional()
    .describe("Maximum characters for context string optimized for LLMs (default: 10000)"),
})

async function tavilySearch(
  query: string,
  numResults: number,
  searchDepth: "basic" | "advanced",
  maxChars: number,
): Promise<string> {
  const apiKey = nextTavilyKey()
  if (!apiKey) throw new Error("No Tavily API key configured")

  const resp = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: apiKey,
      query,
      search_depth: searchDepth,
      max_results: numResults,
      include_answer: true,
      include_raw_content: false,
    }),
    signal: AbortSignal.timeout(30000),
  })

  if (!resp.ok) throw new Error(`Tavily API error: ${resp.status} ${resp.statusText}`)
  const data = (await resp.json()) as {
    answer?: string
    results?: Array<{ title: string; url: string; content: string; score: number }>
  }

  const parts: string[] = []
  if (data.answer) parts.push(`**Summary:** ${data.answer}\n`)

  if (data.results && data.results.length > 0) {
    parts.push("**Results:**\n")
    for (const r of data.results) {
      parts.push(`### ${r.title}\n**URL:** ${r.url}\n${r.content}\n`)
    }
  }

  const combined = parts.join("\n")
  return maxChars > 0 ? combined.slice(0, maxChars) : combined
}

export const WebSearchTool = Tool.define(
  "websearch",
  Effect.gen(function* () {
    const http = yield* HttpClient.HttpClient

    return {
      get description() {
        return DESCRIPTION.replace("{{year}}", new Date().getFullYear().toString())
      },
      parameters: Parameters,
      execute: (params: z.infer<typeof Parameters>, ctx: Tool.Context) =>
        Effect.gen(function* () {
          yield* ctx.ask({
            permission: "websearch",
            patterns: [params.query],
            always: ["*"],
            metadata: {
              query: params.query,
              numResults: params.numResults,
              livecrawl: params.livecrawl,
              type: params.type,
              contextMaxCharacters: params.contextMaxCharacters,
            },
          })

          const numResults = params.numResults ?? 8
          const maxChars = params.contextMaxCharacters ?? 10000
          const searchDepth = params.type === "deep" ? "advanced" : "basic"

          // Try Tavily first; fall back to McpExa if no key or Tavily fails
          const hasTavily = _tavilyKeys.length > 0
          if (hasTavily) {
            const tavilyResult = yield* Effect.tryPromise(() =>
              tavilySearch(params.query, numResults, searchDepth, maxChars),
            ).pipe(
              Effect.catchAll(() =>
                // Tavily failed — fall back to Exa
                McpExa.call(
                  http,
                  "web_search_exa",
                  McpExa.SearchArgs,
                  {
                    query: params.query,
                    type: params.type || "auto",
                    numResults,
                    livecrawl: params.livecrawl || "fallback",
                    contextMaxCharacters: maxChars,
                  },
                  "25 seconds",
                ).pipe(Effect.map((r) => r ?? "No results found.")),
              ),
            )
            return {
              output: tavilyResult || "No search results found. Please try a different query.",
              title: `Web search: ${params.query}`,
              metadata: {},
            }
          }

          // No Tavily key — use Exa
          const result = yield* McpExa.call(
            http,
            "web_search_exa",
            McpExa.SearchArgs,
            {
              query: params.query,
              type: params.type || "auto",
              numResults,
              livecrawl: params.livecrawl || "fallback",
              contextMaxCharacters: maxChars,
            },
            "25 seconds",
          )

          return {
            output: result ?? "No search results found. Please try a different query.",
            title: `Web search: ${params.query}`,
            metadata: {},
          }
        }).pipe(Effect.orDie),
    }
  }),
)
