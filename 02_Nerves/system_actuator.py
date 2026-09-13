"""
02_Nerves/system_actuator.py
Layer 3: Pure OS Execution Layer. Receives verified actions & clean targets.
"""
from __future__ import annotations
import os
import time
import subprocess
import webbrowser
import urllib.parse
import pyautogui

class SystemActuator:
    def __init__(self) -> None:
        pyautogui.FAILSAFE = True
        self.start_menu_dirs = [
            os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs"),
            os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs")
        ]

    def _find_shortcut(self, target: str) -> str | None:
        t = target.lower()
        for base_dir in self.start_menu_dirs:
            if not os.path.exists(base_dir):
                continue
            for root, _, files in os.walk(base_dir):
                for f in files:
                    if f.lower().endswith(".lnk"):
                        name_no_ext = f[:-4].lower()
                        if t == name_no_ext or t in name_no_ext:
                            return os.path.join(root, f)
        return None

    def execute(self, action: str, target: str) -> bool:
        if action == "OPEN":
            # 1. Try Windows Start Menu Link
            lnk = self._find_shortcut(target)
            if lnk:
                try:
                    os.startfile(lnk)
                    return True
                except Exception:
                    pass

            # 2. Try CMD Start
            try:
                res = subprocess.run(f'cmd /c start "" "{target}"', shell=True, capture_output=True)
                if res.returncode == 0:
                    return True
            except Exception:
                pass

            # 3. Native Win Search
            pyautogui.hotkey("win", "s")
            time.sleep(0.35)
            pyautogui.write(target, interval=0.03)
            time.sleep(0.4)
            pyautogui.press("enter")
            return True

        elif action == "CLOSE":
            if any(w in target for w in ["all", "everything", "sab kuch"]):
                pyautogui.hotkey("win", "d")
                return True
            if any(w in target for w in ["this", "current"]):
                pyautogui.hotkey("alt", "f4")
                return True

            exe_map = {
                "chrome": "chrome.exe",
                "unity": "Unity.exe",
                "blender": "blender.exe",
                "store": "WinStore.App.exe",
                "explorer": "explorer.exe",
                "notepad": "notepad.exe",
                "code": "Code.exe"
            }
            exe = exe_map.get(target, f"{target}.exe")
            subprocess.run(f'taskkill /F /IM "{exe}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            pyautogui.hotkey("alt", "f4")
            return True

        elif action == "VOLUME_UP":
            for _ in range(5):
                pyautogui.press("volumeup")
            return True

        elif action == "VOLUME_DOWN":
            for _ in range(5):
                pyautogui.press("volumedown")
            return True

        elif action == "MUTE":
            pyautogui.press("volumemute")
            return True

        elif action == "YOUTUBE":
            if target == "homepage":
                webbrowser.open("https://www.youtube.com")
            else:
                webbrowser.open(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(target)}")
            return True

        elif action == "GOOGLE":
            webbrowser.open(f"https://www.google.com/search?q={urllib.parse.quote_plus(target)}")
            return True

        elif action == "SCREENSHOT":
            pyautogui.screenshot().save(target)
            return True

        return False

actuator = SystemActuator()
