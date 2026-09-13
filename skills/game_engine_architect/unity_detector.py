"""
skills/game_engine_architect/unity_detector.py
Locates and verifies the local Unity 6 engine installation.
"""
import os
from pathlib import Path

DEFAULT_UNITY_PATHS = [
    r"C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe",
    r"C:\Program Files\Unity\Hub\Editor"
]

def get_unity_binary() -> str | None:
    # Direct exact path verification
    exact = Path(r"C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe")
    if exact.exists():
        return str(exact)

    # Search Hub Editor folders
    hub_editor = Path(r"C:\Program Files\Unity\Hub\Editor")
    if hub_editor.exists():
        for exe in hub_editor.glob("*/Editor/Unity.exe"):
            if exe.exists():
                return str(exe)
    return None
