# setup-ultron.ps1
# Run this script ONCE to register 'ultron' as a global command.
# Usage: .\setup-ultron.ps1

$ErrorActionPreference = "Stop"

$packageDir = Join-Path $PSScriptRoot "packages\opencode"

if (-not (Test-Path $packageDir)) {
    Write-Error "Could not find packages\opencode relative to this script. Run from the repo root."
    exit 1
}

Write-Host "Linking 'ultron' globally from: $packageDir" -ForegroundColor Cyan

Set-Location $packageDir

# Try bun link first, fall back to npm link
$bun = Get-Command bun -ErrorAction SilentlyContinue
$npm = Get-Command npm -ErrorAction SilentlyContinue

if ($bun) {
    Write-Host "Using bun link..." -ForegroundColor Yellow
    & bun link
} elseif ($npm) {
    Write-Host "Using npm link..." -ForegroundColor Yellow
    & npm link
} else {
    Write-Error "Neither 'bun' nor 'npm' found. Please install Node.js or Bun first."
    exit 1
}

Write-Host ""
Write-Host "Done! You can now run 'ultron' from any directory." -ForegroundColor Green
Write-Host "Try: ultron --help" -ForegroundColor Green
