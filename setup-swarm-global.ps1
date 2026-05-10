# setup-swarm-global.ps1
# Run this once to make 'swarm' available from any terminal.
# Usage: .\setup-swarm-global.ps1   (run as administrator, or normal user)

$ProjectRoot = "C:\Users\moezf\Desktop\opencode"

Write-Host ""
Write-Host "  Setting up global 'swarm' command..." -ForegroundColor Cyan
Write-Host ""

# ── 1. Create or update PowerShell profile ──────────────────────────────────
$profileDir = Split-Path -Parent $PROFILE
if (-not (Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir -Force | Out-Null }

$pathLine = "`$env:Path += `";$ProjectRoot`""
$profileContent = @"
# Swarm — added by setup-swarm-global.ps1
`$env:Path += ";$ProjectRoot"

"@

if (Test-Path $PROFILE) {
    $existing = Get-Content $PROFILE -Raw
    if ($existing -match [regex]::Escape($pathLine)) {
        Write-Host "  ✅ PowerShell profile already configured" -ForegroundColor Green
    } else {
        Add-Content -Path $PROFILE -Value "`n# Swarm — added by setup-swarm-global.ps1`n$pathLine`n"
        Write-Host "  ✅ Added swarm to PowerShell profile" -ForegroundColor Green
    }
} else {
    Set-Content -Path $PROFILE -Value $profileContent
    Write-Host "  ✅ Created PowerShell profile with swarm PATH" -ForegroundColor Green
}

# ── 2. Also add to system PATH (via registry) for cmd.exe ───────────────────
try {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -split ";" -notcontains $ProjectRoot) {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$ProjectRoot", "User")
        Write-Host "  ✅ Added swarm to User PATH (for cmd.exe)" -ForegroundColor Green
    } else {
        Write-Host "  ✅ User PATH already contains swarm" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠ Could not update system PATH (run as admin for this)" -ForegroundColor Yellow
}

# ── 3. Also make it available in THIS session ────────────────────────────────
$env:Path += ";$ProjectRoot"

Write-Host ""
Write-Host "  ─────────────────────────────────────────────────" -ForegroundColor DarkCyan
Write-Host "  ✅ Setup complete!" -ForegroundColor Cyan
Write-Host "  You can now type 'swarm' in ANY terminal." -ForegroundColor Green
Write-Host ""
Write-Host "  Quick start:"
Write-Host "    swarm          → start orchestrator + open UI"
Write-Host "    swarm.cmd      → same (for cmd.exe)"
Write-Host "    .\swarm.ps1    → same (for PowerShell)"
Write-Host ""
Write-Host "  Restart your terminal or run:" -ForegroundColor Yellow
Write-Host "    `$env:Path += `";$ProjectRoot`"" -ForegroundColor Yellow
Write-Host "  ─────────────────────────────────────────────────" -ForegroundColor DarkCyan
Write-Host ""
