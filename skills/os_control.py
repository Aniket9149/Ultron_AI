"""
skills/os_control.py
System execution & hardware telemetry skill.
"""
from __future__ import annotations
import subprocess

class OSControlSkill:
    @staticmethod
    def execute_powershell(command: str, timeout: int = 15) -> tuple[bool, str]:
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            out = res.stdout.strip()
            err = res.stderr.strip()
            if err and not out:
                return False, f"PowerShell Error: {err}"
            return True, out if out else "Success"
        except subprocess.TimeoutExpired:
            return False, "Command timed out."
        except Exception as exc:
            return False, f"Execution failure: {exc}"

    @staticmethod
    def get_live_battery() -> str:
        cmd = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$p = [System.Windows.Forms.SystemInformation]::PowerStatus; "
            "\"$([int]($p.BatteryLifePercent * 100))% | Status: $($p.PowerLineStatus)\""
        )
        _, out = OSControlSkill.execute_powershell(cmd)
        return out if out else "Unknown"

os_control = OSControlSkill()
