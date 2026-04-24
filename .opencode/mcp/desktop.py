#!/usr/bin/env python3
"""
Ultron Desktop Control MCP
Gives Ultron hands: screenshot, mouse, keyboard, window control.
Requires: pip install mcp pyautogui Pillow pywinauto --break-system-packages
"""
import asyncio
import base64
import io
import subprocess
import sys

try:
    import pyautogui
    import pyautogui as pag
    from PIL import Image
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.1
except ImportError:
    print("Missing deps. Run: pip install pyautogui Pillow --break-system-packages", file=sys.stderr)
    sys.exit(1)

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ultron-desktop")


@mcp.tool()
def screenshot(region: str = "") -> str:
    """
    Take a screenshot of the full desktop or a region.
    region: optional 'x,y,w,h' e.g. '0,0,1920,1080'. Empty = full screen.
    Returns: base64 PNG + dimensions.
    """
    if region:
        x, y, w, h = map(int, region.split(","))
        img = pag.screenshot(region=(x, y, w, h))
    else:
        img = pag.screenshot()

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"SCREENSHOT:{img.size[0]}x{img.size[1]}\nDATA:{b64}"


@mcp.tool()
def mouse_click(x: int, y: int, button: str = "left", clicks: int = 1) -> str:
    """Click at screen coordinates. button: left/right/middle. clicks: 1 or 2 for double-click."""
    pag.click(x, y, button=button, clicks=clicks, interval=0.1)
    return f"Clicked {button}x{clicks} at ({x}, {y})"


@mcp.tool()
def mouse_move(x: int, y: int, duration: float = 0.3) -> str:
    """Move mouse to coordinates without clicking. duration in seconds."""
    pag.moveTo(x, y, duration=duration)
    return f"Mouse moved to ({x}, {y})"


@mcp.tool()
def mouse_drag(from_x: int, from_y: int, to_x: int, to_y: int, duration: float = 0.5) -> str:
    """Drag from one point to another."""
    pag.dragTo(to_x, to_y, duration=duration, button="left")
    return f"Dragged from ({from_x},{from_y}) to ({to_x},{to_y})"


@mcp.tool()
def type_text(text: str, interval: float = 0.03) -> str:
    """Type text at the current cursor position. Use for filling forms, search bars, etc."""
    pag.typewrite(text, interval=interval)
    return f"Typed {len(text)} chars"


@mcp.tool()
def key_press(key: str) -> str:
    """
    Press a keyboard key or shortcut.
    Examples: 'enter', 'escape', 'ctrl+c', 'ctrl+v', 'alt+tab', 'win', 'f5'
    """
    if "+" in key:
        parts = key.split("+")
        pag.hotkey(*parts)
        return f"Hotkey: {key}"
    else:
        pag.press(key)
        return f"Pressed: {key}"


@mcp.tool()
def get_mouse_position() -> str:
    """Get current mouse (x, y) position."""
    x, y = pag.position()
    return f"Mouse at ({x}, {y})"


@mcp.tool()
def get_screen_size() -> str:
    """Get screen resolution."""
    w, h = pag.size()
    return f"Screen: {w}x{h}"


@mcp.tool()
def find_and_click_image(image_path: str, confidence: float = 0.8) -> str:
    """
    Find an image on screen and click it.
    image_path: full path to PNG/JPG to find on screen.
    confidence: 0.0-1.0 match confidence.
    """
    try:
        loc = pag.locateOnScreen(image_path, confidence=confidence)
        if loc is None:
            return f"Image not found on screen: {image_path}"
        center = pag.center(loc)
        pag.click(center)
        return f"Found and clicked image at {center}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def activate_window(title: str) -> str:
    """
    Bring a Windows window to foreground by partial title match.
    Example: activate_window('Notepad'), activate_window('Chrome')
    """
    try:
        import ctypes
        # Use PowerShell to find and activate
        ps = f"""
$wnd = Get-Process | Where-Object {{ $_.MainWindowTitle -like '*{title}*' }} | Select-Object -First 1
if ($wnd) {{
    $sig = '[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);'
    $type = Add-Type -MemberDefinition $sig -Name Win32 -Namespace Utils -PassThru
    $type::SetForegroundWindow($wnd.MainWindowHandle)
    Write-Output "Activated: $($wnd.MainWindowTitle)"
}} else {{
    Write-Output "Window not found: {title}"
}}
"""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or result.stderr.strip() or f"Done"
    except Exception as e:
        return f"Error activating window: {e}"


@mcp.tool()
def list_open_windows() -> str:
    """List all currently open window titles."""
    try:
        ps = "Get-Process | Where-Object { $_.MainWindowTitle } | Select-Object -ExpandProperty MainWindowTitle | Sort-Object"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or "No windows found"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def run_powershell(command: str) -> str:
    """
    Run a PowerShell command and return output.
    Use for Windows-specific automation: opening apps, adjusting settings, etc.
    """
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", command],
            capture_output=True, text=True, timeout=30
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        return out if out else (f"STDERR: {err}" if err else "Done (no output)")
    except subprocess.TimeoutExpired:
        return "Timed out after 30s"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
