"""
05_Actions/action_dispatcher.py
Master Universal Intent Parser & Action Dispatcher.
Routes laptop controls, apps, settings URIs, hardware toggles, and power states.
"""
from __future__ import annotations
import re
import sys
import os
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

system_stats = import_module("05_Actions.system_stats").system_stats
app_launcher = import_module("05_Actions.app_launcher").app_launcher
os_commands = import_module("05_Actions.os_commands").os_commands
hw = import_module("05_Actions.universal_hardware").hardware_ctrl

SETTINGS_DEEP_LINKS = {
    "update": "ms-settings:windowsupdate",
    "wifi": "ms-settings:network-wifi",
    "bluetooth": "ms-settings:bluetooth",
    "hotspot": "ms-settings:network-mobilehotspot",
    "lockscreen": "ms-settings:lockscreen",
    "sound": "ms-settings:sound",
    "display": "ms-settings:display",
    "battery": "ms-settings:batterysaver",
    "storage": "ms-settings:storagesense",
    "apps": "ms-settings:appsfeatures",
    "touchpad": "ms-settings:devices-touchpad",
    "printer": "ms-settings:printers",
    "time": "ms-settings:dateandtime",
    "vpn": "ms-settings:network-vpn"
}

class ActionDispatcher:
    def parse_and_execute(self, command: str) -> tuple[bool, str]:
        cmd = command.lower().strip()

        # 1. BRIGHTNESS (e.g. "brightness 80", "brightness badha", "kam kar")
        bright_match = re.search(r'brightness\s*(\d+)', cmd)
        if bright_match:
            return hw.set_brightness(int(bright_match.group(1)))
        if "brightness" in cmd:
            if any(w in cmd for w in ["full", "100", "badha", "increase"]):
                return hw.set_brightness(100)
            if any(w in cmd for w in ["zero", "kam", "low", "decrease"]):
                return hw.set_brightness(25)

        # 2. POWER MANAGEMENT (Sleep, Shutdown, Restart, Cancel)
        if any(w in cmd for w in ["cancel shutdown", "shutdown cancel", "abort shutdown"]):
            return hw.abort_shutdown()
        if any(w in cmd for w in ["sleep", "so ja", "sleep mode"]):
            return hw.sleep_pc()
        if any(w in cmd for w in ["restart", "reboot"]):
            return hw.restart_pc()
        if any(w in cmd for w in ["shutdown", "power off", "laptop band kar"]):
            return hw.shutdown_pc()
        if any(w in cmd for w in ["lock pc", "lock system", "screen lock"]):
            return os_commands.lock_workstation()

        # 3. RADIOS & CONNECTIVITY (Wi-Fi, Bluetooth, Airplane)
        if "wifi" in cmd or "wi-fi" in cmd or "internet" in cmd:
            if any(w in cmd for w in ["on", "chalu", "enable", "start"]):
                return hw.toggle_wifi(True)
            if any(w in cmd for w in ["off", "band", "disable"]):
                return hw.toggle_wifi(False)
            return True, hw.toggle_wifi(True)[1]

        if "bluetooth" in cmd:
            if any(w in cmd for w in ["on", "chalu", "enable"]):
                return hw.toggle_bluetooth(True)
            if any(w in cmd for w in ["off", "band", "disable"]):
                return hw.toggle_bluetooth(False)
            return True, hw.toggle_bluetooth(True)[1]

        if any(w in cmd for w in ["airplane mode", "flight mode"]):
            return hw.toggle_airplane_mode()

        # 4. AUDIO & MUTE
        if any(w in cmd for w in ["mute", "unmute", "awaaz band", "sound off"]):
            return hw.mute_audio()

        vol_match = re.search(r'volume\s*(\d+)', cmd)
        if vol_match:
            return os_commands.set_volume(int(vol_match.group(1)))

        # 5. DISPLAY MODES & NIGHT LIGHT
        if any(w in cmd for w in ["night light", "blue light", "night mode"]):
            return hw.toggle_night_light()
        if any(w in cmd for w in ["duplicate screen", "screen mirror"]):
            return hw.set_projection_mode("duplicate")
        if any(w in cmd for w in ["extend screen", "second screen"]):
            return hw.set_projection_mode("extend")

        # 6. SYSTEM UTILITIES (Screenshot, Task Manager, Device Manager)
        if any(w in cmd for w in ["screenshot", "screen shot", "snip"]):
            return hw.take_screenshot()
        if any(w in cmd for w in ["task manager", "taskmgr", "processes"]):
            return hw.open_task_manager()
        if any(w in cmd for w in ["device manager"]):
            return hw.open_device_manager()

        # 7. CLEANUP & MAINTENANCE
        if any(w in cmd for w in ["clean", "temp", "kachra", "recycle bin", "free space"]):
            return hw.clean_temp_files()
        if any(w in cmd for w in ["flush dns", "dns clear"]):
            return hw.flush_dns()

        # 8. TELEMETRY & SPECS
        if any(w in cmd for w in ["status", "report", "ram", "cpu", "battery", "performance"]):
            return True, f"System telemetry: {system_stats.get_summary_text()}"

        # 9. DYNAMIC SETTINGS ROUTER (Hotspot, Touchpad, Printers, Time, etc.)
        if "setting" in cmd:
            for key, uri in SETTINGS_DEEP_LINKS.items():
                if key in cmd:
                    os.system(f"start {uri}")
                    return True, f"Windows Settings ({key}) open kar di."
            os.system("start ms-settings:")
            return True, "Main Windows Settings open kar di."

        # 10. APP LIFECYCLE (Open / Close)
        open_match = re.search(r'(?:open|kholo|start)\s+([a-zA-Z0-9\s]+)', cmd)
        if open_match:
            return app_launcher.open_app(open_match.group(1).strip())

        close_match = re.search(r'(?:close|band\s*karo|kill)\s+([a-zA-Z0-9\s]+)', cmd)
        if close_match:
            return app_launcher.close_app(close_match.group(1).strip())

        return False, ""

action_dispatcher = ActionDispatcher()
