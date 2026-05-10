# True Swarm — Start Script
# Runs the FastAPI orchestrator on port 8000

$Root    = Split-Path -Parent $MyInvocation.MyCommand.Path
$SwarmRoot = $Root  # script lives inside swarm/
$Venv    = Join-Path $SwarmRoot "venv\Scripts\python.exe"
$Python  = if (Test-Path $Venv) { $Venv } else { "python" }

Write-Host ""
Write-Host "  TRUE SWARM" -ForegroundColor Magenta
Write-Host "  Starting orchestrator on http://localhost:8000" -ForegroundColor DarkMagenta
Write-Host ""

# Install deps if uvicorn missing
try {
    & $Python -c "import uvicorn" 2>$null
} catch {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & $Python -m pip install fastapi uvicorn httpx --quiet
}

# Run from swarm root so relative imports work
Set-Location $SwarmRoot
&amp; $Python -m uvicorn orchestrator:app --host 0.0.0.0 --port 8000 --reload
