"""Standalone tests for relative cursor intent routing."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "02_Brain" / "cursor_router.py"
SPEC = importlib.util.spec_from_file_location("cursor_router", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CursorRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.screen = MagicMock()
        self.screen.size.return_value = (1920, 1080)

    def test_resolves_all_relative_zones(self) -> None:
        cases = {
            "move cursor to center": ("center", 960, 540),
            "mouse le jao left": ("left", 288, 540),
            "pointer shift right": ("right", 1632, 540),
            "cursor upar karo": ("top", 960, 162),
            "mouse neeche rakho": ("bottom", 960, 918),
        }

        for command, (zone, expected_x, expected_y) in cases.items():
            with self.subTest(command=command):
                self.assertEqual(
                    MODULE.extract_cursor_intent(command, self.screen),
                    {"action": "MOVE_CURSOR", "x": expected_x, "y": expected_y, "zone": zone},
                )

    def test_rejects_non_pointer_or_non_movement_text(self) -> None:
        self.assertIsNone(MODULE.extract_cursor_intent("open the browser", self.screen))
        self.assertIsNone(MODULE.extract_cursor_intent("move the window", self.screen))
        self.assertIsNone(MODULE.extract_cursor_intent(None, self.screen))
        self.screen.size.assert_not_called()


if __name__ == "__main__":
    unittest.main()