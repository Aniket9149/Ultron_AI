"""Grounded foreground and running-window inspection for Windows."""

from __future__ import annotations

from typing import Any

import pygetwindow as gw


class SurfaceInspector:
    """Read visible desktop surfaces through the operating-system window list."""

    def __init__(self) -> None:
        self.ignored_titles = {
            "",
            "Default IME",
            "MSCTFIME UI",
            "Program Manager",
            "Settings",
            "Windows Input Experience",
        }

    def get_active_window(self) -> str:
        """Return the title of the currently focused foreground window."""
        window = gw.getActiveWindow()
        title = getattr(window, "title", "") if window is not None else ""
        return title.strip() if title else "Unknown"

    def get_running_surfaces(self) -> list[str]:
        """Return unique, non-minimized application titles."""
        clean: list[str] = []
        for window in gw.getAllWindows():
            title = getattr(window, "title", "").strip()
            if (
                title
                and title not in self.ignored_titles
                and len(title) > 2
                and not getattr(window, "isMinimized", False)
                and title not in clean
            ):
                clean.append(title)
        return clean

    def summarize_view(self) -> str:
        """Construct an accurate description from current OS window state."""
        active = self.get_active_window()
        open_apps = self.get_running_surfaces()

        if not open_apps:
            return "Screen par filhal koi major window active nahi hai."

        apps_string = ", ".join(open_apps[:4])
        return f"Currently active window '{active}' hai, aur samne ye apps open hain: {apps_string}."


surface_inspector = SurfaceInspector()