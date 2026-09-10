"""Standalone tests for generic application and UI operation."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "03_Automation_Engines" / "universal_operator.py"
SPEC = importlib.util.spec_from_file_location("universal_operator", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UniversalOperatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ui = MagicMock()
        self.bus = MagicMock()
        self.window_api = MagicMock()
        self.input_api = MagicMock()
        self.operator = MODULE.UniversalOperator(self.ui, self.bus, self.window_api, self.input_api)

    def test_focuses_existing_matching_window(self) -> None:
        window = MagicMock(title="Editor - ULTRON", isMinimized=True)
        self.window_api.getAllWindows.return_value = [window]

        with patch.object(MODULE.time, "sleep"):
            self.assertTrue(self.operator.open_any_app("editor"))

        window.restore.assert_called_once_with()
        window.activate.assert_called_once_with()
        self.input_api.press.assert_not_called()

    def test_launches_unmatched_app_through_search(self) -> None:
        self.window_api.getAllWindows.return_value = []

        with patch.object(MODULE.time, "sleep"):
            self.assertTrue(self.operator.open_any_app("Calculator"))

        self.input_api.press.assert_any_call("win")
        self.input_api.write.assert_called_once_with("Calculator", interval=0.03)
        self.input_api.press.assert_any_call("enter")

    def test_publishes_grounded_click_and_rejects_missing_target(self) -> None:
        self.ui.locate_active_text.return_value = (120, 70)
        self.assertTrue(self.operator.click_element("Submit"))
        self.bus.publish.assert_called_once_with(
            "MOTOR_DIRECTIVE",
            {"action": "CLICK_COORDS", "data": {"x": 120, "y": 70}},
        )

        self.ui.locate_active_text.return_value = None
        self.assertFalse(self.operator.click_element("Missing"))


if __name__ == "__main__":
    unittest.main()