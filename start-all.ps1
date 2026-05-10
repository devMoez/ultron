# Ultron — Start Everything
# Launches Cortex, swarm, tracker dashboard, tasksync, then Ultron TUI

$Root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv   = Join-Path $Root "swarm\venv\Scripts\python.exe"
$Node   = "node"
$Cortex = "C:\Users\moezf\Desktop\Cortex"

Write-Host ""
Write-Host "  ULTRON - STARTING ALL SERVICES" -ForegroundColor Cyan
Write-Host ""

# 0. Cortex (architectural awareness engine — must be up before coding starts)
Write-Host "  [0] Starting Cortex..." -ForegroundColor Magenta
Start-Process -FilePath "$Cortex\internal_brain\mind.exe" `
    -ArgumentList "$Cortex" `
    -WorkingDirectory $Cortex `
    -WindowStyle Minimized
Start-Sleep -Seconds 1
Start-Process -FilePath "$Cortex\cortex.exe" `
    -WorkingDirectory $Cortex `
    -WindowStyle Minimized
Start-Sleep -Seconds 1
Write-Host "        Cortex live on http://localhost:8080" -ForegroundColor DarkMagenta

# 1. True Swarm (blackboard engine on port 8000)
Write-Host "  [1] Starting True Swarm..." -ForegroundColor Yellow
$SwarmVenv = Join-Path $Root "swarm\venv\Scripts\python.exe"
$SwarmPy   = if (Test-Path $SwarmVenv) { $SwarmVenv } else { "python" }
Start-Process -FilePath $SwarmPy `
    -ArgumentList "-m uvicorn orchestrator:app --host 0.0.0.0 --port 8000" `
    -WorkingDirectory (Join-Path $Root "swarm") `
    -WindowStyle Minimized

Start-Sleep -Seconds 2

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
