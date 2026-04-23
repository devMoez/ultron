import z from "zod"
import { Effect } from "effect"
import { exec } from "child_process"
import { promisify } from "util"
import os from "os"
import * as Tool from "./tool"

const execAsync = promisify(exec)

const Parameters = z.object({
  category: z
    .enum(["all", "cpu", "memory", "disk", "os", "network", "processes", "battery"])
    .default("all")
    .describe("What system info to retrieve. Use 'all' for a full overview."),
  topN: z
    .number()
    .optional()
    .default(10)
    .describe("For 'processes' category: how many top processes to show (by CPU usage). Default 10."),
})

const DESCRIPTION = `Get detailed system information about the computer.

Categories:
- "all": Full system overview (OS, CPU, memory, disk)
- "cpu": CPU model, cores, usage percentage
- "memory": RAM total, used, free
- "disk": Disk drives, capacity, free space
- "os": Operating system, hostname, uptime, username
- "network": IP addresses, network interfaces
- "processes": Top running processes by CPU usage
- "battery": Battery status (laptops)

Use this to answer questions like "how much RAM do I have?", "what's my CPU?", "is my disk almost full?", "what processes are running?"`

async function getWindowsInfo(category: string, topN: number): Promise<string> {
  const lines: string[] = []

  if (category === "all" || category === "os") {
    const { stdout } = await execAsync(
      "powershell -NoProfile -Command \"Get-ComputerInfo | Select-Object WindowsProductName,OsVersion,OsArchitecture,CsName,CsProcessors,OsLastBootUpTime | ConvertTo-Json\"",
    )
    try {
      const info = JSON.parse(stdout.trim())
      lines.push("=== Operating System ===")
      lines.push(`OS:           ${info.WindowsProductName}`)
      lines.push(`Version:      ${info.OsVersion}`)
      lines.push(`Architecture: ${info.OsArchitecture}`)
      lines.push(`Hostname:     ${info.CsName}`)
      lines.push(`Last Boot:    ${info.OsLastBootUpTime}`)
      lines.push(`Username:     ${os.userInfo().username}`)
      lines.push(`Uptime:       ${Math.floor(os.uptime() / 3600)}h ${Math.floor((os.uptime() % 3600) / 60)}m`)
    } catch {
      lines.push("=== Operating System ===")
      lines.push(stdout.trim())
    }
  }

  if (category === "all" || category === "cpu") {
    try {
      const { stdout } = await execAsync(
        "powershell -NoProfile -Command \"Get-WmiObject Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors,LoadPercentage | ConvertTo-Json\"",
      )
      const cpu = JSON.parse(stdout.trim())
      const cpuData = Array.isArray(cpu) ? cpu[0] : cpu
      lines.push("\n=== CPU ===")
      lines.push(`Model:            ${cpuData.Name?.trim()}`)
      lines.push(`Physical Cores:   ${cpuData.NumberOfCores}`)
      lines.push(`Logical Cores:    ${cpuData.NumberOfLogicalProcessors}`)
      lines.push(`Current Load:     ${cpuData.LoadPercentage}%`)
    } catch {
      const cpus = os.cpus()
      lines.push("\n=== CPU ===")
      lines.push(`Model:  ${cpus[0]?.model ?? "Unknown"}`)
      lines.push(`Cores:  ${cpus.length}`)
    }
  }

  if (category === "all" || category === "memory") {
    const totalMB = Math.round(os.totalmem() / 1024 / 1024)
    const freeMB = Math.round(os.freemem() / 1024 / 1024)
    const usedMB = totalMB - freeMB
    const pct = Math.round((usedMB / totalMB) * 100)
    lines.push("\n=== Memory (RAM) ===")
    lines.push(`Total:  ${(totalMB / 1024).toFixed(1)} GB`)
    lines.push(`Used:   ${(usedMB / 1024).toFixed(1)} GB  (${pct}%)`)
    lines.push(`Free:   ${(freeMB / 1024).toFixed(1)} GB`)
  }

  if (category === "all" || category === "disk") {
    try {
      const { stdout } = await execAsync(
        "powershell -NoProfile -Command \"Get-PSDrive -PSProvider FileSystem | Select-Object Name,Used,Free | ConvertTo-Json\"",
      )
      const drives = JSON.parse(stdout.trim())
      const driveList = Array.isArray(drives) ? drives : [drives]
      lines.push("\n=== Disk Drives ===")
      for (const d of driveList) {
        if (d.Used == null && d.Free == null) continue
        const used = d.Used ? (d.Used / 1024 / 1024 / 1024).toFixed(1) : "?"
        const free = d.Free ? (d.Free / 1024 / 1024 / 1024).toFixed(1) : "?"
        const total = d.Used && d.Free ? ((d.Used + d.Free) / 1024 / 1024 / 1024).toFixed(1) : "?"
        lines.push(`${d.Name}:\\  Total: ${total} GB  Used: ${used} GB  Free: ${free} GB`)
      }
    } catch {
      lines.push("\n=== Disk ===")
      lines.push("Could not retrieve disk info.")
    }
  }

  if (category === "network") {
    const ifaces = os.networkInterfaces()
    lines.push("=== Network Interfaces ===")
    for (const [name, addresses] of Object.entries(ifaces)) {
      for (const addr of addresses ?? []) {
        if (addr.internal) continue
        lines.push(`${name}: ${addr.address} (${addr.family})`)
      }
    }
  }

  if (category === "processes") {
    const { stdout } = await execAsync(
      `powershell -NoProfile -Command "Get-Process | Sort-Object CPU -Descending | Select-Object -First ${topN} Name,CPU,WorkingSet | ConvertTo-Json"`,
    )
    try {
      const procs = JSON.parse(stdout.trim())
      const procList = Array.isArray(procs) ? procs : [procs]
      lines.push(`=== Top ${topN} Processes (by CPU) ===`)
      lines.push(`${"Name".padEnd(30)} ${"CPU(s)".padStart(10)} ${"Memory(MB)".padStart(12)}`)
      lines.push("-".repeat(55))
      for (const p of procList) {
        const name = String(p.Name ?? "").padEnd(30)
        const cpu = String(Math.round(p.CPU ?? 0)).padStart(10)
        const mem = String(Math.round((p.WorkingSet ?? 0) / 1024 / 1024)).padStart(12)
        lines.push(`${name} ${cpu} ${mem}`)
      }
    } catch {
      lines.push(stdout.trim())
    }
  }

  if (category === "battery") {
    const { stdout } = await execAsync(
      "powershell -NoProfile -Command \"Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining,BatteryStatus | ConvertTo-Json\"",
    )
    try {
      const bat = JSON.parse(stdout.trim())
      lines.push("=== Battery ===")
      lines.push(`Charge:  ${bat.EstimatedChargeRemaining ?? "N/A"}%`)
      const status: Record<number, string> = { 1: "Discharging", 2: "AC Power", 3: "Fully Charged", 4: "Low", 5: "Critical" }
      lines.push(`Status:  ${status[bat.BatteryStatus] ?? "Unknown"}`)
    } catch {
      lines.push("=== Battery ===\nNo battery detected or not available.")
    }
  }

  return lines.join("\n")
}

export const SystemInfoTool = Tool.define(
  "system_info",
  Effect.succeed({
    description: DESCRIPTION,
    parameters: Parameters,
    execute: (params: z.infer<typeof Parameters>, _ctx: Tool.Context) =>
      Effect.tryPromise(async () => {
        const platform = os.platform()
        let output: string

        if (platform === "win32") {
          output = await getWindowsInfo(params.category, params.topN ?? 10)
        } else {
          // Fallback for non-Windows: use os module data
          const totalMB = Math.round(os.totalmem() / 1024 / 1024)
          const freeMB = Math.round(os.freemem() / 1024 / 1024)
          const cpus = os.cpus()
          output = [
            `OS:       ${os.type()} ${os.release()} (${os.arch()})`,
            `Hostname: ${os.hostname()}`,
            `Uptime:   ${Math.floor(os.uptime() / 3600)}h ${Math.floor((os.uptime() % 3600) / 60)}m`,
            `CPU:      ${cpus[0]?.model} (${cpus.length} cores)`,
            `RAM:      ${(totalMB / 1024).toFixed(1)} GB total, ${(freeMB / 1024).toFixed(1)} GB free`,
          ].join("\n")
        }

        return {
          title: `System info (${params.category})`,
          output,
          metadata: { category: params.category, platform },
        }
      }),
  }),
)
