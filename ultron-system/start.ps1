# Ultron Master Dashboard — Launch Script
# Pauses on crash so you can read the error.

$Root    = Split-Path -Parent $MyInvocation.MyCommand.Path
$Venv    = Join-Path $Root "..\swarm\venv"
$Python  = Join-Path $Venv "Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "Python venv not found at $Python" -ForegroundColor Red
    Write-Host "Run: python -m venv $Venv && $Venv\Scripts\pip install -r $Root\requirements.txt"
    Read-Host "Press Enter to exit"
    exit 1
}

# Install requirements if needed
$ReqFile = Join-Path $Root "requirements.txt"
& $Python -m pip install -r $ReqFile --quiet

Write-Host ""
Write-Host "  ULTRON MASTER DASHBOARD" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:5010" -ForegroundColor Green
Write-Host ""

Push-Location $Root
& $Python (Join-Path $Root "main.py")
$code = $LASTEXITCODE
Pop-Location

if ($code -ne 0) {
    Write-Host ""
    Write-Host "Dashboard crashed with exit code $code." -ForegroundColor Red
    Write-Host "Press any key to close..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
