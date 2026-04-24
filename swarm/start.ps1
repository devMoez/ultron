# Ultron Swarm – start.ps1
# Usage: powershell -ExecutionPolicy Bypass -File .\start.ps1

$SwarmRoot = $PSScriptRoot
$VenvDir   = Join-Path $SwarmRoot "venv"
$Python    = Join-Path $VenvDir "Scripts\python.exe"
$Req       = Join-Path $SwarmRoot "requirements.txt"
$LogsDir   = Join-Path $SwarmRoot "logs"

Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Ultron Swarm Startup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan

# ── Kill existing swarm processes ──────────────────────────────────────────
Write-Host "[1/4] Stopping existing swarm processes..." -ForegroundColor Yellow
$scripts = @("orchestrator.py","planner.py","designer.py","builder.py","debugger.py","verifier.py")
Get-Process python -ErrorAction SilentlyContinue | ForEach-Object {
    $cmd = (Get-WmiObject Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue).CommandLine
    foreach ($s in $scripts) {
        if ($cmd -like "*$s*") {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            Write-Host "  Killed: $s (pid $($_.Id))" -ForegroundColor DarkGray
        }
    }
}
Start-Sleep -Milliseconds 500

# ── Create/activate venv ───────────────────────────────────────────────────
Write-Host "[2/4] Checking Python venv..." -ForegroundColor Yellow
if (-not (Test-Path $Python)) {
    Write-Host "  Creating venv at $VenvDir ..." -ForegroundColor DarkGray
    python -m venv $VenvDir
    Write-Host "  Installing requirements (using python -m pip)..." -ForegroundColor DarkGray
    & $Python -m pip install --quiet --upgrade pip 2>&1 | Out-Null
    & $Python -m pip install --quiet -r $Req
    Write-Host "  Dependencies installed." -ForegroundColor Green
} else {
    Write-Host "  Venv found." -ForegroundColor DarkGray
}

# ── Init DB ────────────────────────────────────────────────────────────────
Write-Host "[3/4] Initializing database..." -ForegroundColor Yellow
& $Python (Join-Path $SwarmRoot "setup_db.py")

# ── Start orchestrator (which spawns agents) ───────────────────────────────
Write-Host "[4/4] Starting orchestrator..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

$orchLog    = Join-Path $LogsDir "orchestrator.log"
$orchLogErr = Join-Path $LogsDir "orchestrator.err.log"
Start-Process -FilePath $Python `
    -ArgumentList (Join-Path $SwarmRoot "orchestrator.py") `
    -WorkingDirectory $SwarmRoot `
    -RedirectStandardOutput $orchLog `
    -RedirectStandardError  $orchLogErr `
    -WindowStyle Hidden

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
Write-Host "  Swarm started!" -ForegroundColor Green
Write-Host "  Orchestrator → http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "  Logs → $LogsDir" -ForegroundColor Green
Write-Host ""
Write-Host "  Drop tasks into:" -ForegroundColor Cyan
Write-Host "  $SwarmRoot\tasks\queue\" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Example task (save as task_001.json):" -ForegroundColor Cyan
Write-Host '  {"target_agent":"planner","description":"build a login page","project_path":""}' -ForegroundColor DarkGray
Write-Host "═══════════════════════════════════════════" -ForegroundColor Green
