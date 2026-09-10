"""Standalone tests for LifePulse action dispatch without hardware."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "life_pulse.py"
SPEC = importlib.util.spec_from_file_location("life_pulse", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["life_pulse"] = MODULE
SPEC.loader.exec_module(MODULE)


class LifePulseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = MODULE.RuntimeComponents(
            synapse=MagicMock(),
            vocals=MagicMock(),
            spine=MagicMock(),
            inspector=MagicMock(),
            operator=MagicMock(),
            brain=MagicMock(),
            wake_core=MagicMock(),
        )

    def test_dispatches_move_and_vocal_confirmation_over_bus(self) -> None:
        MODULE.dispatch_action(
            {"action": "MOVE_CURSOR", "x": 100, "y": 200, "response": "Moving"},
            self.runtime,
        )
        self.runtime.synapse.publish.assert_any_call("VOCAL_IMPULSE", {"text": "Moving"})
        self.runtime.synapse.publish.assert_any_call(
            "MOTOR_DIRECTIVE",
            {"action": "MOVE_CURSOR", "data": {"x": 100, "y": 200}},
        )
        self.runtime.operator.assert_not_called()

    def test_dispatches_open_inspect_hotkey_and_click_failure(self) -> None:
        self.runtime.operator.click_element.return_value = False
        self.runtime.inspector.summarize_view.return_value = "visible"
        MODULE.dispatch_action({"action": "OPEN_APP", "target": "editor"}, self.runtime)
        MODULE.dispatch_action({"action": "CLICK_UI", "target": "submit"}, self.runtime)
        MODULE.dispatch_action({"action": "INSPECT_SCREEN"}, self.runtime)
        MODULE.dispatch_action({"action": "HOTKEY", "keys": ["ctrl", "l"]}, self.runtime)

        self.runtime.operator.open_any_app.assert_called_once_with("editor")
        self.runtime.operator.click_element.assert_called_once_with("submit")
        self.runtime.inspector.summarize_view.assert_called_once_with()
        self.runtime.synapse.publish.assert_any_call("MOTOR_DIRECTIVE", {"action": "HOTKEY", "data": {"keys": ["ctrl", "l"]}})


if __name__ == "__main__":
    unittest.main()