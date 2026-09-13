"""
05_Actions/app_launcher.py
Windows application lifecycle management for Ultron OS.
"""
from __future__ import annotations
import subprocess
import psutil

APP_REGISTRY = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "calc": "calc.exe",
    "cmd": "cmd.exe",
    "terminal": "wt.exe",
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "spotify": "spotify.exe",
    "code": "code.cmd"
}

class AppLauncher:
    @staticmethod
    def open_app(app_name: str) -> tuple[bool, str]:
        target = app_name.lower().strip()
        exe = APP_REGISTRY.get(target, target)
        try:
            subprocess.Popen(exe, shell=True)
            return True, f"{app_name} khol diya hai."
        except Exception as exc:
            return False, f"{app_name} kholne me error aaya: {exc}"

    @staticmethod
    def close_app(process_name: str) -> tuple[bool, str]:
        target = process_name.lower().strip()
        target_exe = APP_REGISTRY.get(target, f"{target}.exe" if not target.endswith(".exe") else target)

        killed = False
        for proc in psutil.process_iter(['name']):
            try:
                pname = proc.info.get('name')
                if pname and pname.lower() == target_exe.lower():
                    proc.terminate()
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except Exception:
                continue

        if killed:
            return True, f"{process_name} ko band kar diya."
        return False, f"{process_name} running nahi mila."

app_launcher = AppLauncher()
