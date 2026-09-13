"""
05_Actions/system_stats.py
Hardware and telemetry reader for Ultron OS.
"""
from __future__ import annotations
import psutil

class SystemStats:
    @staticmethod
    def get_cpu_ram() -> dict[str, float]:
        cpu_usage = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory()
        return {
            "cpu_percent": cpu_usage,
            "ram_percent": ram.percent,
            "ram_free_gb": round(ram.available / (1024 ** 3), 2)
        }

    @staticmethod
    def get_battery() -> dict[str, any]:
        battery = psutil.sensors_battery()
        if not battery:
            return {"has_battery": False, "percent": 100, "charging": True}
        return {
            "has_battery": True,
            "percent": battery.percent,
            "charging": battery.power_plugged
        }

    @staticmethod
    def get_summary_text() -> str:
        stats = SystemStats.get_cpu_ram()
        batt = SystemStats.get_battery()
        batt_str = f", Battery: {batt['percent']}%" if batt['has_battery'] else ""
        return f"CPU: {stats['cpu_percent']}%, RAM used: {stats['ram_percent']}% ({stats['ram_free_gb']}GB free){batt_str}"

system_stats = SystemStats()
