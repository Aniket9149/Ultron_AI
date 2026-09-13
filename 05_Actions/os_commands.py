"""
05_Actions/os_commands.py
Hardware control and OS system power operations.
Uses modern pycaw API with fallback for Windows endpoint volume.
"""
from __future__ import annotations
import ctypes

class OsCommands:
    @staticmethod
    def lock_workstation() -> tuple[bool, str]:
        try:
            ctypes.windll.user32.LockWorkStation()
            return True, "PC lock kar diya."
        except Exception as exc:
            return False, f"Lock nahi ho paya: {exc}"

    @staticmethod
    def set_volume(level: int) -> tuple[bool, str]:
        try:
            from pycaw.pycaw import AudioUtilities
            devices = AudioUtilities.GetSpeakers()
            # Modern pycaw compatibility
            if hasattr(devices, "EndpointVolume"):
                volume = devices.EndpointVolume
            else:
                from pycaw.pycaw import IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))

            clamped = max(0, min(100, level))
            scalar = clamped / 100.0
            volume.SetMasterVolumeLevelScalar(scalar, None)
            return True, f"Volume {clamped}% par set kar diya."
        except Exception as exc:
            return False, f"Volume change error: {exc}"

os_commands = OsCommands()
