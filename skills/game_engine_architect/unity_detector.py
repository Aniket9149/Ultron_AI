"""
Unity 6 and Unity Hub Path Detector.
"""
from pathlib import Path

UNITY_HUB_PATHS = [
    Path(r"C:\Program Files\Unity Hub\Unity Hub.exe"),
    Path(r"C:\Program Files (x86)\Unity Hub\Unity Hub.exe")
]

UNITY_EDITOR_PATHS = [
    Path(r"C:\Program Files\Unity\Hub\Editor\6000.5.5f1\Editor\Unity.exe"),
    Path(r"C:\Program Files\Unity\Hub\Editor\6000.0.34f1\Editor\Unity.exe"),
    Path(r"C:\Program Files\Unity\Hub\Editor\6000.0.0f1\Editor\Unity.exe")
]

def get_unity_hub_binary() -> Path | None:
    for p in UNITY_HUB_PATHS:
        if p.exists():
            return p
    return None

def get_unity_binary() -> Path | None:
    # Check editor paths directly
    for p in UNITY_EDITOR_PATHS:
        if p.exists():
            return p
    # Fallback search inside Unity Hub editor directory
    hub_editors = Path(r"C:\Program Files\Unity\Hub\Editor")
    if hub_editors.exists():
        for ed in hub_editors.glob("*/Editor/Unity.exe"):
            return ed
    return None
