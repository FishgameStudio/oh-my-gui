# Audio media player module.

import os
import sys
import subprocess
import threading
from logging import info, warning, error, critical

info(f"Module {__name__} loaded")

def play_audio(file_path: str, *, sync: bool = False) -> None:
    """Play mp3 or wav"""
    def _play():
        system = sys.platform
        
        # ========== WAV ==========
        if file_path.lower().endswith(".wav"):
            if system == "win32":
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
            elif system == "darwin":  # macOS
                subprocess.run(["afplay", file_path], capture_output=True)
            elif system.startswith("linux"):
                subprocess.run(["aplay", file_path], capture_output=True)
            return

        # ========== MP3 ==========
        if file_path.lower().endswith(".mp3"):
            if system == "win32":
                # Windows Insider player
                subprocess.run(["powershell", "-c", f"(New-Object Media.SoundPlayer '{file_path}').PlaySync();"], capture_output=True)
            elif system == "darwin":
                # the builtin of macOS `afplay` support mp3
                subprocess.run(["afplay", file_path], capture_output=True)
            elif system.startswith("linux"):
                # Most versions of Linux has ffplay / play
                try:
                    subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], capture_output=True)
                except FileNotFoundError:
                    subprocess.run(["play", file_path], capture_output=True)
            return
    if sync:
        _play()
    else:
        threading.Thread(target=_play, daemon=True).start()

# Test

if __name__ == '__main__':
    if sys.platform.startswith('win'):
        play_audio("C:\\Windows\\Media\\Alarm06.wav", sync=True)
    else:
        pass