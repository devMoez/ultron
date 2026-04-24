# Ultron Discord Bot — Launch Script
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host "  ULTRON DISCORD BOT" -ForegroundColor Cyan
Write-Host "  Starting..." -ForegroundColor Green
Write-Host ""

Push-Location $Root
bun run --env-file .env src/index.ts
$code = $LASTEXITCODE
Pop-Location

if ($code -ne 0) {
    Write-Host ""
    Write-Host "Bot crashed with exit code $code." -ForegroundColor Red
    Write-Host "Press any key to close..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
