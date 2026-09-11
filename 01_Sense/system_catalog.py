"""Cached local Windows application catalog used before any app launch."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
from typing import Any

try:
    import winreg
except ImportError:  # pragma: no cover - non-Windows development environments
    winreg = None


class SystemCatalog:
    """Index Start Menu entries, uninstall records, and resolvable executables."""

    ALIASES = {
        "vs code": "visual studio code",
        "vscode": "visual studio code",
        "code": "visual studio code",
        "edge": "msedge",
        "notepad": "notepad.exe",
    }

    def __init__(self, scan: bool = True) -> None:
        self._entries: dict[str, str] = {}
        if scan:
            self.refresh()

    def refresh(self) -> None:
        self._entries.clear()
        start_menu_roots = (
            Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
            / "Microsoft/Windows/Start Menu/Programs",
            Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs",
        )
        for root in start_menu_roots:
            self._scan_shortcuts(root)
        self._scan_uninstall_keys()
        for executable in ("notepad.exe", "msedge.exe", "code.exe", "calc.exe"):
            resolved = shutil.which(executable)
            if resolved:
                self._add(Path(executable).stem, resolved)
                self._add(Path(executable).name, resolved)

    def is_app_installed(self, query: str) -> tuple[bool, str]:
        """Return whether *query* resolves to a locally indexed app path."""
        normalized = self._normalize(query)
        if not normalized:
            return False, ""
        alias = self.ALIASES.get(normalized, normalized)
        direct = shutil.which(query) or shutil.which(f"{query}.exe")
        if direct:
            return True, direct
        if alias in self._entries:
            return True, self._entries[alias]
        for name, path in self._entries.items():
            if alias == name or alias in name or name in alias:
                return True, path
        return False, ""

    def _scan_shortcuts(self, root: Path) -> None:
        if not root.exists():
            return
        for path in root.rglob("*"):
            if path.suffix.casefold() in {".lnk", ".url", ".exe"}:
                self._add(path.stem, str(path))

    def _scan_uninstall_keys(self) -> None:
        if winreg is None:
            return
        locations = (
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
        )
        for hive, location in locations:
            try:
                with winreg.OpenKey(hive, location) as root:
                    for index in range(winreg.QueryInfoKey(root)[0]):
                        try:
                            with winreg.OpenKey(root, winreg.EnumKey(root, index)) as entry:
                                display_name = self._registry_value(entry, "DisplayName")
                                install_location = self._registry_value(entry, "InstallLocation")
                                display_icon = self._registry_value(entry, "DisplayIcon")
                                candidate = display_icon or install_location
                                if display_name and candidate:
                                    self._add(display_name, candidate.split(",", 1)[0].strip('"'))
                        except OSError:
                            continue
            except OSError:
                continue

    @staticmethod
    def _registry_value(key: Any, name: str) -> str:
        try:
            return str(winreg.QueryValueEx(key, name)[0]).strip()
        except OSError:
            return ""

    def _add(self, name: str, path: str) -> None:
        normalized = self._normalize(name)
        if normalized and path:
            self._entries.setdefault(normalized, path)

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(str(value).casefold().replace(".lnk", "").split())


system_catalog = SystemCatalog()