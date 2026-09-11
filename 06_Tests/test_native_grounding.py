"""Standalone tests for Windows UIA grounding with fake accessibility trees."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "01_Sense" / "native_grounding.py"


class Rectangle:
    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class FakeElement:
    def __init__(self, name: str, automation_id: str, rectangle: Rectangle) -> None:
        self.name = name
        self.id = automation_id
        self.bounds = rectangle

    def window_text(self) -> str:
        return self.name

    def automation_id(self) -> str:
        return self.id

    def rectangle(self) -> Rectangle:
        return self.bounds


class FakeWindow:
    def __init__(self, title: str, elements: list[FakeElement]) -> None:
        self.title = title
        self.elements = elements

    def window_text(self) -> str:
        return self.title

    def descendants(self) -> list[FakeElement]:
        return self.elements


class FakeDesktop:
    def __init__(self, windows: list[FakeWindow]) -> None:
        self._windows = windows

    def windows(self) -> list[FakeWindow]:
        return self._windows


FAKE_GW = types.ModuleType("pygetwindow")
FAKE_PYWINAUTO = types.ModuleType("pywinauto")
FAKE_PYWINAUTO.Desktop = MagicMock()
ORIGINAL_GW = sys.modules.get("pygetwindow")
ORIGINAL_PYWINAUTO = sys.modules.get("pywinauto")
sys.modules["pygetwindow"] = FAKE_GW
sys.modules["pywinauto"] = FAKE_PYWINAUTO
SPEC = importlib.util.spec_from_file_location("native_grounding", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
if ORIGINAL_GW is None:
    sys.modules.pop("pygetwindow", None)
else:
    sys.modules["pygetwindow"] = ORIGINAL_GW
if ORIGINAL_PYWINAUTO is None:
    sys.modules.pop("pywinauto", None)
else:
    sys.modules["pywinauto"] = ORIGINAL_PYWINAUTO


class NativeGroundingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.element = FakeElement("New Tab", "tabstrip_new_tab_button", Rectangle(100, 50, 140, 90))
        self.window = FakeWindow("Chrome - ULTRON", [self.element])
        self.desktop = FakeDesktop([self.window])
        self.grounding = MODULE.NativeUIGrounding(desktop=self.desktop)

    def test_resolves_element_center_by_name_or_automation_id(self) -> None:
        self.assertEqual(self.grounding.get_element_coords("chrome", "new tab"), (120, 70))
        self.assertEqual(self.grounding.get_element_coords("chrome", "tabstrip"), (120, 70))

    def test_new_tab_fallback_and_missing_window(self) -> None:
        self.assertEqual(self.grounding.get_new_tab_button(), (120, 70))
        self.assertIsNone(self.grounding.get_element_coords("edge", "missing"))

    def test_locates_text_in_active_window(self) -> None:
        FAKE_GW.getActiveWindowTitle = MagicMock(return_value="Chrome - ULTRON")
        self.assertEqual(self.grounding.locate_active_text("new tab"), (120, 70))


if __name__ == "__main__":
    unittest.main()