# Ultron — Start Everything
# Launches swarm, tracker dashboard, tasksync, then Ultron TUI

$Root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv   = Join-Path $Root "swarm\venv\Scripts\python.exe"
$Node   = "node"

Write-Host ""
Write-Host "  ULTRON - STARTING ALL SERVICES" -ForegroundColor Cyan
Write-Host ""

# 1. Swarm orchestrator + agents
Write-Host "  [1] Starting Swarm..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$Root\swarm\start.ps1`"" -WindowStyle Minimized

Start-Sleep -Seconds 2

# 2. Ultron Tracker Dashboard
Write-Host "  [2] Starting Ultron Tracker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$Root\ultron-system\start.ps1`"" -WindowStyle Minimized

Start-Sleep -Seconds 1

# 3. TaskSync MCP (HTTP server on :3011)
Write-Host "  [3] Starting TaskSync MCP..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Minimized -Command `"npx -y tasksync-mcp-http`"" -WindowStyle Minimized

Start-Sleep -Seconds 2

# 4. Ultron TUI (foreground)
Write-Host "  [4] Starting Ultron..." -ForegroundColor Green
Write-Host ""
Set-Location $Root
& npx ultron

Write-Host ""
Write-Host "Ultron exited. Press any key to close." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
