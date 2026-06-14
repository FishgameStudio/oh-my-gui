# Other utils.

import os
import subprocess
from sys import platform
import pyperclip
from pathlib import Path
import requests
from typing import Any
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

def get_environment_variable(key: str, default: str | None = None) -> str:
    """Get an environment variable or return a default value if not found."""
    return os.getenv(key, default if default is not None else "")
def set_clip(text: str, /, *, strip: bool = True, encoding: str = "utf-8", errors: str = "strict"):
    """Set the clipboard content with optional text processing."""
    if strip:
        text = text.strip()
    pyperclip.copy(text.encode(encoding, errors=errors).decode())
def get_clip() -> str:
    """Get the clipboard content."""
    return pyperclip.paste()
def get_user_root_dir() -> str:
    """Get the root directory of the current user."""
    return str(Path.home())
def send_system_notification(title_: str, text_: str, /) -> None:
    """Send a notification to the system."""
    title = title_.replace('"', '\\"')
    text = text_.replace('"', '\\"')
    if platform.startswith("win"):
        cmd = f'''
        $title = "{title}"
        $msg = "{text}"
        Add-Type -AssemblyName System.Windows.Forms
        $notify = New-Object System.Windows.Forms.NotifyIcon
        $notify.Icon = [System.Drawing.Icon]::FromHandle(([System.Drawing.SystemIcons]::Information).Handle)
        $notify.BalloonTipTitle = $title
        $notify.BalloonTipText = $msg
        $notify.BalloonTipIcon = "Info"
        $notify.Visible = $true
        $notify.ShowBalloonTip(5000)
        Start-Sleep 5
        $notify.Dispose()
        '''
        subprocess.run(
            ["powershell", "-Command", cmd],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )

    elif platform == "Darwin":
        script = f'display notification "{text}" with title "{title}"'
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )

    elif platform == "Linux":
        subprocess.run(
            ["notify-send", title, text],
            capture_output=True,
            text=True
        )



# Test
if __name__ == '__main__':
    send_system_notification("Title", "TextTextTextText")