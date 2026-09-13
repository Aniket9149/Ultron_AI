"""
05_Actions/autonomous_core.py
Full Administrative Execution Layer for Ultron OS.
Grants raw PowerShell, WMI hardware queries, and registry control.
"""
from __future__ import annotations
import subprocess

class AutonomousCore:
    @staticmethod
    def execute_powershell(command: str, timeout: int = 15) -> tuple[bool, str]:
        """Runs raw administrative PowerShell command with standard output capture."""
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
            return True, out if out else "Command executed successfully."
        except subprocess.TimeoutExpired:
            return False, "Command timed out."
        except Exception as exc:
            return False, f"Execution failure: {exc}"

    @staticmethod
    def inspect_system(query_target: str) -> str:
        """Inspects deep OS and hardware components via WMI."""
        target = query_target.lower().strip()
        queries = {
            "usb": "Get-PnpDevice -PresentOnly | Where-Object { $_.InstanceId -match '^USB' } | Select-Object FriendlyName, Status",
            "services": "Get-Service | Where-Object { $_.Status -eq 'Running' } | Select-Object -First 10 DisplayName",
            "firewall": "Get-NetFirewallProfile | Select-Object Name, Enabled",
            "network": "Get-NetIPConfiguration | Select-Object InterfaceAlias, IPv4Address",
            "disks": "Get-Volume | Select-Object DriveLetter, FileSystemLabel, SizeRemaining, Size"
        }
        cmd = queries.get(target, f"Get-CimInstance -ClassName {query_target}")
        _, output = AutonomousCore.execute_powershell(cmd)
        return output

autonomous_core = AutonomousCore()
