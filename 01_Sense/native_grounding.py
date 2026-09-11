# -*- coding: utf-8 -*-
"""
ULTRON NATIVE UI ACCESSIBILITY GROUNDING (01_Sense)
Extracts exact center coordinates of UI elements via Windows UIA.
"""
import sys
from typing import Any

# Preserve the apartment-threaded mode before comtypes or pywinauto imports.
sys.coinit_flags = 2

try:
    import comtypes
except Exception:
    pass

import pygetwindow as gw
from pywinauto import Desktop

class NativeUIGrounding:
    def __init__(self, desktop: Any = None):
        self.desktop = desktop if desktop is not None else Desktop(backend="uia")

    def get_element_coords(self, window_keyword: str, target_name: str) -> tuple:
        """Scans the target window tree and returns exact (x, y) coordinates."""
        try:
            target_win = None
            for w in self.desktop.windows():
                if window_keyword.lower() in w.window_text().lower():
                    target_win = w
                    break

            if not target_win:
                return None

            elements = target_win.descendants()
            clean_target = target_name.lower().strip()

            for elem in elements:
                try:
                    name = elem.window_text().lower()
                    auto_id = elem.automation_id().lower()

                    if clean_target in name or clean_target in auto_id:
                        rect = elem.rectangle()
                        cx = (rect.left + rect.right) // 2
                        cy = (rect.top + rect.bottom) // 2
                        if cx > 0 and cy > 0:
                            print(f"[UIA GROUNDING]: Located '{elem.window_text()}' at ({cx}, {cy})")
                            return (cx, cy)
                except Exception:
                    continue
        except Exception as e:
            print(f"[UIA ERROR]: {e}")

        return None

    def get_new_tab_button(self) -> tuple:
        """Universal target resolver for browser New Tab / Plus buttons."""
        for kw in ["brave", "chrome", "edge"]:
            for label in ["new tab", "add new tab", "+", "tabstrip_new_tab_button"]:
                coords = self.get_element_coords(kw, label)
                if coords:
                    return coords
        return None

    def locate_active_text(self, text: str) -> tuple:
        """Locates any text or button matching query in current foreground window."""
        active = gw.getActiveWindowTitle()
        if not active:
            return None
        return self.get_element_coords(active[:15], text)

native_grounding = NativeUIGrounding()
