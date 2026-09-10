"""Exact Windows UI Automation grounding for visible interface elements."""

from __future__ import annotations

from typing import Any

import pygetwindow as gw
from pywinauto import Desktop


class NativeUIGrounding:
    """Resolve accessible UI element names to screen-center coordinates."""

    def __init__(self, desktop: Any | None = None) -> None:
        self.desktop = desktop if desktop is not None else Desktop(backend="uia")

    def get_element_coords(self, window_keyword: str, target_name: str) -> tuple[int, int] | None:
        """Scan the matching window tree and return an element's center point."""
        try:
            target_window = next(
                (
                    window
                    for window in self.desktop.windows()
                    if window_keyword.casefold() in window.window_text().casefold()
                ),
                None,
            )
            if target_window is None:
                return None

            clean_target = target_name.casefold().strip()
            for element in target_window.descendants():
                try:
                    name = element.window_text().casefold()
                    automation_id = element.automation_id().casefold()
                    if clean_target not in name and clean_target not in automation_id:
                        continue

                    rectangle = element.rectangle()
                    center_x = (rectangle.left + rectangle.right) // 2
                    center_y = (rectangle.top + rectangle.bottom) // 2
                    if center_x > 0 and center_y > 0:
                        print(
                            f"[UIA GROUNDING]: Located '{element.window_text()}' "
                            f"at ({center_x}, {center_y})"
                        )
                        return center_x, center_y
                except Exception:
                    continue
        except Exception as exc:
            print(f"[UIA ERROR]: {exc}")
        return None

    def get_new_tab_button(self) -> tuple[int, int] | None:
        """Resolve a browser new-tab control across common accessible labels."""
        for window_keyword in ("brave", "chrome", "edge"):
            for target_name in ("new tab", "add new tab", "+", "tabstrip_new_tab_button"):
                coordinates = self.get_element_coords(window_keyword, target_name)
                if coordinates is not None:
                    return coordinates
        return None

    def locate_active_text(self, text: str) -> tuple[int, int] | None:
        """Locate text or a button in the current foreground window."""
        get_active_title = getattr(gw, "getActiveWindowTitle", None)
        if get_active_title is not None:
            active_title = get_active_title()
        else:
            active_window = gw.getActiveWindow()
            active_title = getattr(active_window, "title", "") if active_window else ""
        if not active_title:
            return None
        return self.get_element_coords(active_title[:15], text)


native_grounding = NativeUIGrounding()