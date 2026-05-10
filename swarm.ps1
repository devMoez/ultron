# swarm.ps1
# Global Swarm Launch Command
# Usage: .\swarm.ps1  (or type 'swarm' from any terminal if swarm.cmd is in PATH)

$SwarmDir = "C:\Users\moezf\Desktop\opencode\swarm"
$Python   = "python"

# Try venv python first
$VenvPy = Join-Path $SwarmDir "venv\Scripts\python.exe"
if (Test-Path $VenvPy) { $Python = $VenvPy }

Write-Host ""
Write-Host "  SWARM" -ForegroundColor Cyan
Write-Host "  Starting orchestrator + UI on http://localhost:8000" -ForegroundColor DarkCyan
Write-Host ""

# Ensure uvicorn is installed
try {
    & $Python -c "import uvicorn" 2>$null
} catch {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & $Python -m pip install fastapi uvicorn httpx --quiet
}

# Kill any existing orchestrator on port 8000
$existing = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "  Port 8000 in use - stopping existing process..." -ForegroundColor Yellow
    $existing.OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Seconds 1
}

# Start orchestrator in background
$logFile = Join-Path $SwarmDir "orchestrator.log"
$errFile = Join-Path $SwarmDir "orchestrator_err.log"
$proc = Start-Process -FilePath $Python `
    -ArgumentList "-m uvicorn orchestrator:app --host 127.0.0.1 --port 8000 --log-level warning" `
    -WorkingDirectory $SwarmDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError $errFile `
    -PassThru

# Wait for it to start
$started = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Milliseconds 500
    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:8000/status" -UseBasicParsing -TimeoutSec 1
        if ($resp.StatusCode -eq 200) { $started = $true; break }
    } catch {}
}

if ($started) {
    Write-Host "  [OK] Swarm orchestrator is running (PID $($proc.Id))" -ForegroundColor Green
    Write-Host "  Opening UI at http://localhost:8000" -ForegroundColor Cyan
    Start-Process "http://localhost:8000"
} else {
    Write-Host "  [FAILED] Could not start orchestrator within 7.5s" -ForegroundColor Red
    Write-Host "  Check error log:" -ForegroundColor DarkRed
    Write-Host "    $errFile" -ForegroundColor DarkRed
    Get-Content $errFile -Tail 5 -ErrorAction SilentlyContinue
}

