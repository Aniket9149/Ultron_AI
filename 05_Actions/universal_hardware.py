"""
05_Actions/universal_hardware.py
Comprehensive Windows Laptop Controller.
Covers: Brightness, Power States, Display Modes, Radios, Audio, and OS Maintenance.
"""
from __future__ import annotations
import os
import re
import ctypes
import subprocess
import webbrowser

class UniversalHardware:
    # --- 1. DISPLAY & BRIGHTNESS ---
    @staticmethod
    def set_brightness(level: int) -> tuple[bool, str]:
        """Sets laptop internal display brightness (0-100) via WMI."""
        clamped = max(0, min(100, level))
        ps = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {clamped})"
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=4)
            return True, f"Brightness {clamped}% set kar di."
        except Exception as exc:
            return False, f"Brightness change fail: {exc}"

    @staticmethod
    def toggle_night_light() -> tuple[bool, str]:
        os.system("start ms-settings:nightlight")
        return True, "Night Light settings khol di hai."

    @staticmethod
    def set_projection_mode(mode: str) -> tuple[bool, str]:
        """Modes: duplicate, extend, internal (pc only), external (second screen only)."""
        valid = {"duplicate": "/clone", "extend": "/extend", "pc": "/internal", "second": "/external"}
        flag = valid.get(mode.lower(), "/extend")
        os.system(f"displayswitch.exe {flag}")
        return True, f"Display mode '{mode}' apply kar diya."

    # --- 2. POWER & BATTERY ---
    @staticmethod
    def sleep_pc() -> tuple[bool, str]:
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return True, "Laptop sleep mode me daal diya."
        except Exception as exc:
            return False, f"Sleep command fail: {exc}"

    @staticmethod
    def restart_pc(delay: int = 5) -> tuple[bool, str]:
        os.system(f"shutdown /r /t {delay}")
        return True, f"System {delay} seconds me restart hoga."

    @staticmethod
    def shutdown_pc(delay: int = 10) -> tuple[bool, str]:
        os.system(f"shutdown /s /t {delay}")
        return True, f"System {delay} seconds me shutdown hoga."

    @staticmethod
    def abort_shutdown() -> tuple[bool, str]:
        os.system("shutdown /a")
        return True, "Shutdown cancel kar diya."

    # --- 3. HARDWARE RADIOS (Wi-Fi, Bluetooth, Airplane) ---
    @staticmethod
    def toggle_wifi(state: bool) -> tuple[bool, str]:
        action = "enabled" if state else "disabled"
        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", f'netsh interface set interface name="Wi-Fi" admin={action}'],
                capture_output=True,
                timeout=4
            )
            return True, f"Wi-Fi {'On' if state else 'Off'} kar diya."
        except Exception:
            os.system("start ms-settings:network-wifi")
            return True, "Wi-Fi settings page open kiya."

    @staticmethod
    def toggle_bluetooth(state: bool) -> tuple[bool, str]:
        target = "On" if state else "Off"
        ps = f"""
        [Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
        $r = [Windows.Devices.Radios.Radio]::GetRadiosAsync().GetAwaiter().GetResult() | Where-Object {{ $_.Kind -eq 'Bluetooth' }}
        if ($r) {{ $r.SetStateAsync('{target}').GetAwaiter().GetResult() | Out-Null }}
        """
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=5)
            return True, f"Bluetooth {target} kiya."
        except Exception:
            os.system("start ms-settings:bluetooth")
            return True, "Bluetooth settings khol di."

    @staticmethod
    def toggle_airplane_mode() -> tuple[bool, str]:
        os.system("start ms-settings:network-airplanemode")
        return True, "Airplane mode toggle khol diya."

    # --- 4. AUDIO & MUTE CONTROLS ---
    @staticmethod
    def mute_audio() -> tuple[bool, str]:
        # VK_VOLUME_MUTE = 0xAD
        ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
        return True, "Master audio mute/unmute toggle kar diya."

    # --- 5. SYSTEM UTILITIES & SCREENSHOT ---
    @staticmethod
    def take_screenshot() -> tuple[bool, str]:
        # Win + Shift + S snippet tool
        os.system("start ms-screenclip:")
        return True, "Screen snipping tool khol diya."

    @staticmethod
    def open_task_manager() -> tuple[bool, str]:
        os.system("start taskmgr.exe")
        return True, "Task Manager khol diya."

    @staticmethod
    def open_device_manager() -> tuple[bool, str]:
        os.system("start devmgmt.msc")
        return True, "Device Manager khol diya."

    # --- 6. SYSTEM CLEANUP & NETWORK ---
    @staticmethod
    def flush_dns() -> tuple[bool, str]:
        os.system("ipconfig /flushdns")
        return True, "DNS cache flush kar diya."

    @staticmethod
    def clean_temp_files() -> tuple[bool, str]:
        ps = 'Remove-Item -Path "$env:TEMP\\*" -Recurse -Force -ErrorAction SilentlyContinue; Clear-RecycleBin -Force -ErrorAction SilentlyContinue'
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps], creationflags=subprocess.CREATE_NO_WINDOW)
        return True, "Temp files aur Recycle Bin background me clean ho rahe hain."

hardware_ctrl = UniversalHardware()
