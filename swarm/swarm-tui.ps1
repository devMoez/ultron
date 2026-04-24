$SwarmRoot = "C:\Users\moezf\Desktop\opencode\swarm"
$Python    = Join-Path $SwarmRoot "venv\Scripts\python.exe"
Set-Location $SwarmRoot
& $Python (Join-Path $SwarmRoot "swarm_tui.py")
