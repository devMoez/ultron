#!/usr/bin/env python3
"""
Ultron TaskSync MCP
Gives Ultron the ability to pause and ask Moez for help when stuck.
Requires: pip install mcp --break-system-packages
"""
import asyncio
import subprocess
import sys
import time
import os
import json
from datetime import datetime
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing mcp. Run: pip install mcp --break-system-packages", file=sys.stderr)
    sys.exit(1)

mcp = FastMCP("ultron-tasksync")

# State file so questions persist across tool calls
STATE_FILE = Path(os.path.expanduser("~")) / "Desktop" / "opencode" / ".opencode" / "mcp" / "tasksync_queue.json"


def _load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"pending": [], "answered": []}


def _save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _show_windows_dialog(title: str, message: str) -> str:
    """Show a PowerShell input dialog and return user's answer."""
    # Use InputBox (VBScript via PowerShell) for a real text-input popup
    ps = f"""
Add-Type -AssemblyName Microsoft.VisualBasic
$answer = [Microsoft.VisualBasic.Interaction]::InputBox(
    "{message.replace('"', "'").replace(chr(10), ' ')}",
    "Ultron Needs Help — {title.replace('"', "'")}",
    ""
)
Write-Output $answer
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=300  # 5 minute timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT: No answer received within 5 minutes"
    except Exception as e:
        return f"ERROR: {e}"


@mcp.tool()
def ask_human(question: str, context: str = "", urgency: str = "normal") -> str:
    """
    Pause and ask Moez a question when Ultron is stuck or needs clarification.

    question: The specific question to ask.
    context: Optional background info to include in the popup.
    urgency: 'normal' or 'blocking' (blocking shows a more urgent dialog).

    Returns the user's answer. Use this when:
    - You're about to do something irreversible and aren't sure
    - You're missing information needed to complete a task
    - You hit an error you can't resolve alone
    - You need a decision between multiple paths
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    full_message = question
    if context:
        full_message = f"{context}\n\n{question}"

    # Log to state file
    state = _load_state()
    entry = {
        "id": f"q_{int(time.time())}",
        "timestamp": timestamp,
        "question": question,
        "context": context,
        "urgency": urgency,
        "status": "pending"
    }
    state["pending"].append(entry)
    _save_state(state)

    # Show dialog to user
    answer = _show_windows_dialog(
        title=f"Question [{timestamp}]",
        message=full_message
    )

    # Update state
    entry["answer"] = answer
    entry["status"] = "answered"
    state["pending"] = [e for e in state["pending"] if e["id"] != entry["id"]]
    state["answered"].append(entry)
    _save_state(state)

    if not answer:
        return "User dismissed the dialog without answering. Treat as 'skip' or use your best judgment."

    return f"User answered: {answer}"


@mcp.tool()
def notify_human(title: str, message: str, importance: str = "info") -> str:
    """
    Send a desktop notification to Moez — without blocking.
    Use this to report task completion, warnings, or status updates.

    importance: 'info', 'warning', or 'error' (changes the icon)
    """
    icon_map = {
        "info": "Information",
        "warning": "Exclamation",
        "error": "Hand"
    }
    icon = icon_map.get(importance, "Information")

    ps = f"""
Add-Type -AssemblyName System.Windows.Forms
$n = New-Object System.Windows.Forms.NotifyIcon
$n.Icon = [System.Drawing.SystemIcons]::{icon}
$n.BalloonTipTitle = "Ultron: {title.replace('"', "'")}"
$n.BalloonTipText = "{message.replace('"', "'")[:200]}"
$n.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::{icon}
$n.Visible = $true
$n.ShowBalloonTip(5000)
Start-Sleep -Seconds 6
$n.Dispose()
"""
    try:
        subprocess.Popen(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps]
        )
        return f"Notification sent: {title}"
    except Exception as e:
        return f"Notification failed: {e}"


@mcp.tool()
def get_pending_questions() -> str:
    """Check if there are any unanswered questions in the queue."""
    state = _load_state()
    pending = state.get("pending", [])
    if not pending:
        return "No pending questions."
    lines = [f"[{q['timestamp']}] {q['question']}" for q in pending]
    return f"{len(pending)} pending:\n" + "\n".join(lines)


@mcp.tool()
def confirm_action(action_description: str, consequence: str = "") -> str:
    """
    Ask Moez to confirm before doing something potentially destructive.
    Returns 'confirmed' or 'cancelled'.

    action_description: What Ultron is about to do.
    consequence: What will happen if confirmed (e.g., 'This will delete 50 files').
    """
    msg = f"Ultron wants to:\n{action_description}"
    if consequence:
        msg += f"\n\nConsequence: {consequence}"
    msg += "\n\nType YES to confirm, anything else to cancel."

    answer = _show_windows_dialog("Confirm Action", msg)

    if answer and answer.strip().upper() == "YES":
        return "confirmed"
    return f"cancelled (user said: '{answer}')"


if __name__ == "__main__":
    mcp.run()
