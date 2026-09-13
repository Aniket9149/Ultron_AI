"""
05_Actions/universal_os.py
Universal Windows Automation Engine using native URI protocols and PowerShell.
"""
from __future__ import annotations
import os
import subprocess
import webbrowser

# Universal Windows Settings Deep Links (URI schemes)
SETTINGS_MAP = {
    "update": "ms-settings:windowsupdate",
    "windows update": "ms-settings:windowsupdate",
    "lock screen": "ms-settings:lockscreen",
    "bluetooth": "ms-settings:bluetooth",
    "wifi": "ms-settings:network-wifi",
    "network": "ms-settings:network",
    "display": "ms-settings:display",
    "sound": "ms-settings:sound",
    "battery": "ms-settings:batterysaver",
    "apps": "ms-settings:appsfeatures",
    "storage": "ms-settings:storagesense",
    "about": "ms-settings:about"
}

class UniversalOS:
    @staticmethod
    def open_settings_page(page_keyword: str) -> tuple[bool, str]:
        """Opens specific Windows settings page directly via URI."""
        key = page_keyword.lower().strip()
        uri = SETTINGS_MAP.get(key)
        
        # If not exact match, check substring
        if not uri:
            for name, link in SETTINGS_MAP.items():
                if name in key or key in name:
                    uri = link
                    break
                    
        if not uri:
            uri = "ms-settings:"  # Default main settings

        try:
            os.system(f"start {uri}")
            return True, f"Windows Settings ({key}) khol di hai."
        except Exception as exc:
            return False, f"Settings kholne me error: {exc}"

    @staticmethod
    def trigger_windows_update() -> tuple[bool, str]:
        """Directly opens update page and triggers check if possible."""
        try:
            os.system("start ms-settings:windowsupdate")
            # PowerShell command to initiate scan in background
            ps_cmd = "(New-Object -ComObject Microsoft.Update.AutoUpdate).DetectNow()"
            subprocess.Popen(["powershell", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
            return True, "Windows Update trigger kar diya aur settings screen khol di."
        except Exception as exc:
            return False, f"Update fail hua: {exc}"

    @staticmethod
    def run_powershell(command: str) -> tuple[bool, str]:
        """Safely executes dynamic PowerShell command."""
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                timeout=10
            )
            output = result.stdout.strip() or result.stderr.strip()
            return True, output if output else "Command execute ho gaya."
        except Exception as exc:
            return False, f"Execution failed: {exc}"

    @staticmethod
    def open_url_or_search(query: str) -> tuple[bool, str]:
        """Handles web search or URL opening universally."""
        query = query.strip()
        if query.startswith("http://") or query.startswith("https://"):
            webbrowser.open(query)
            return True, f"Opening {query}"
        else:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return True, f"Google par '{query}' search kar raha hoon."

    @staticmethod
    def empty_recycle_bin() -> tuple[bool, str]:
        cmd = "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"
        return UniversalOS.run_powershell(cmd)

universal_os = UniversalOS()
