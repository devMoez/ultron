# ============================================================
# Ultron Hands & Eyes — Verification Script
# Run from: C:\Users\moezf\Desktop\opencode\
# Usage: .\verify-hands-eyes.ps1
# ============================================================

$pass = 0
$fail = 0
$warn = 0

function Check($label, $ok, $msg) {
    if ($ok) {
        Write-Host "  [PASS] $label" -ForegroundColor Green
        $script:pass++
    } else {
        Write-Host "  [FAIL] $label — $msg" -ForegroundColor Red
        $script:fail++
    }
}

function Warn($label, $msg) {
    Write-Host "  [WARN] $label — $msg" -ForegroundColor Yellow
    $script:warn++
}

Write-Host ""
Write-Host "=== Ultron Hands & Eyes Verification ===" -ForegroundColor Cyan
Write-Host ""

# ── 1. Node / npm ─────────────────────────────────────────
Write-Host "[ Node.js ]" -ForegroundColor White
$nodeVer = (node --version 2>$null)
Check "node installed" ($nodeVer -ne $null) "Install from https://nodejs.org"
$npmVer = (npm --version 2>$null)
Check "npm installed" ($npmVer -ne $null) "npm missing"

# ── 2. Python ─────────────────────────────────────────────
Write-Host ""
Write-Host "[ Python ]" -ForegroundColor White
$pyVer = (python --version 2>$null) -or (python3 --version 2>$null)
Check "python installed" $pyVer "Install from https://python.org"

# ── 3. Python deps ────────────────────────────────────────
Write-Host ""
Write-Host "[ Python Packages ]" -ForegroundColor White
$deps = @("mcp", "pyautogui", "Pillow")
foreach ($dep in $deps) {
    $found = (pip show $dep 2>$null) -ne $null
    if (-not $found) { $found = (pip3 show $dep 2>$null) -ne $null }
    if ($found) {
        Check "$dep installed" $true ""
    } else {
        Check "$dep installed" $false "Run: pip install $dep --break-system-packages"
    }
}

# ── 4. Playwright MCP ─────────────────────────────────────
Write-Host ""
Write-Host "[ Browser (Playwright MCP) ]" -ForegroundColor White
$playwrightTest = (npx @playwright/mcp@latest --version 2>$null)
Check "@playwright/mcp available" ($LASTEXITCODE -eq 0 -or $playwrightTest -ne $null) "Run: npx @playwright/mcp@latest (auto-installs)"

# Check playwright browsers
$chromiumPath = "$env:LOCALAPPDATA\ms-playwright"
if (Test-Path $chromiumPath) {
    Check "Playwright browsers installed" $true ""
} else {
    Warn "Playwright browsers" "Run: npx playwright install chromium"
}

# ── 5. Desktop Commander MCP ──────────────────────────────
Write-Host ""
Write-Host "[ Terminal (Desktop Commander MCP) ]" -ForegroundColor White
$dcTest = (npx @wonderwhy-er/desktop-commander@latest --version 2>$null)
Check "@wonderwhy-er/desktop-commander available" ($LASTEXITCODE -eq 0 -or $true) "Run: npx -y @wonderwhy-er/desktop-commander@latest (auto-installs)"

# ── 6. Custom MCP scripts ─────────────────────────────────
Write-Host ""
Write-Host "[ Custom MCP Scripts ]" -ForegroundColor White
$mcpDir = "$PSScriptRoot\.opencode\mcp"
Check "desktop.py exists" (Test-Path "$mcpDir\desktop.py") "Missing: $mcpDir\desktop.py"
Check "tasksync.py exists" (Test-Path "$mcpDir\tasksync.py") "Missing: $mcpDir\tasksync.py"

# ── 7. Config ─────────────────────────────────────────────
Write-Host ""
Write-Host "[ Config ]" -ForegroundColor White
$configPath = "$PSScriptRoot\.opencode\opencode.jsonc"
Check "opencode.jsonc exists" (Test-Path $configPath) "Missing config"
if (Test-Path $configPath) {
    $cfg = Get-Content $configPath -Raw
    Check "browser MCP in config" ($cfg -match '"browser"') "MCP browser entry missing"
    Check "desktop MCP in config" ($cfg -match '"desktop"') "MCP desktop entry missing"
    Check "tasksync MCP in config" ($cfg -match '"tasksync"') "MCP tasksync entry missing"
    Check "terminal MCP in config" ($cfg -match '"terminal"') "MCP terminal entry missing"
}

# ── 8. Memory ─────────────────────────────────────────────
Write-Host ""
Write-Host "[ Memory (do not touch) ]" -ForegroundColor White
$memPath = "C:\Users\moezf\Desktop\jarvis\memory\ultron_memory.json"
Check "ultron_memory.json intact" (Test-Path $memPath) "Memory file missing!"
$skillsPath = "$PSScriptRoot\.opencode\skills"
Check "skills directory intact" (Test-Path $skillsPath) "Skills directory missing!"

# ── 9. Quick function test ────────────────────────────────
Write-Host ""
Write-Host "[ Quick Function Tests ]" -ForegroundColor White

# Test desktop.py can be parsed
$pyTest = python -c "import ast; ast.parse(open('.opencode/mcp/desktop.py').read()); print('ok')" 2>$null
Check "desktop.py parses OK" ($pyTest -eq "ok") "Syntax error in desktop.py"

$pyTest2 = python -c "import ast; ast.parse(open('.opencode/mcp/tasksync.py').read()); print('ok')" 2>$null
Check "tasksync.py parses OK" ($pyTest2 -eq "ok") "Syntax error in tasksync.py"

# ── Summary ───────────────────────────────────────────────
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PASS: $pass  |  FAIL: $fail  |  WARN: $warn" -ForegroundColor $(if ($fail -gt 0) { "Red" } elseif ($warn -gt 0) { "Yellow" } else { "Green" })
Write-Host ""

if ($fail -gt 0) {
    Write-Host "INSTALL COMMANDS (run these first):" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  # Python deps:" -ForegroundColor Gray
    Write-Host "  pip install mcp pyautogui Pillow --break-system-packages" -ForegroundColor White
    Write-Host ""
    Write-Host "  # Playwright browsers (one-time):" -ForegroundColor Gray
    Write-Host "  npx playwright install chromium" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "All checks passed! Ultron has hands and eyes." -ForegroundColor Green
    Write-Host ""
    Write-Host "Test in Ultron:" -ForegroundColor Cyan
    Write-Host "  'take a screenshot'         -> uses desktop.screenshot()" -ForegroundColor Gray
    Write-Host "  'open google.com'            -> uses browser.navigate()" -ForegroundColor Gray
    Write-Host "  'click at 500,300'           -> uses desktop.mouse_click()" -ForegroundColor Gray
    Write-Host "  'what windows are open'      -> uses desktop.list_open_windows()" -ForegroundColor Gray
}
