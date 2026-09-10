"""Standalone tests for grounded surface inspection."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "01_Sense" / "surface_inspector.py"
FAKE_GW = types.ModuleType("pygetwindow")
SPEC = importlib.util.spec_from_file_location("surface_inspector", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)


class SurfaceInspectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.active_window = MagicMock(title="  Browser - ULTRON  ")
        self.windows = [
            MagicMock(title="  Browser - ULTRON  ", isMinimized=False),
            MagicMock(title="Editor", isMinimized=False),
            MagicMock(title="Editor", isMinimized=False),
            MagicMock(title="Settings", isMinimized=False),
            MagicMock(title="Hidden App", isMinimized=True),
            MagicMock(title="", isMinimized=False),
            MagicMock(title="x", isMinimized=False),
        ]
        FAKE_GW.getActiveWindow = MagicMock(return_value=self.active_window)
        FAKE_GW.getAllWindows = MagicMock(return_value=self.windows)
        with patch.dict(sys.modules, {"pygetwindow": FAKE_GW}):
            SPEC.loader.exec_module(MODULE)
        self.inspector = MODULE.SurfaceInspector()

    def test_reads_active_and_filters_running_surfaces(self) -> None:
        self.assertEqual(self.inspector.get_active_window(), "Browser - ULTRON")
        self.assertEqual(self.inspector.get_running_surfaces(), ["Browser - ULTRON", "Editor"])

    def test_summary_is_grounded_in_window_titles(self) -> None:
        self.assertEqual(
            self.inspector.summarize_view(),
            "Currently active window 'Browser - ULTRON' hai, aur samne ye apps open hain: Browser - ULTRON, Editor.",
        )

    def test_missing_active_window_and_empty_surface_list(self) -> None:
        FAKE_GW.getActiveWindow.return_value = None
        FAKE_GW.getAllWindows.return_value = []
        self.assertEqual(self.inspector.get_active_window(), "Unknown")
        self.assertEqual(self.inspector.summarize_view(), "Screen par filhal koi major window active nahi hai.")


if __name__ == "__main__":
    unittest.main()