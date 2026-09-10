"""Standalone verification for ReflexSpine directive routing."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "04_Spine" / "reflex_planner.py"
SPEC = importlib.util.spec_from_file_location("reflex_planner", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReflexSpineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bus = MagicMock()
        self.motor = MagicMock()
        self.spine = MODULE.ReflexSpine(bus=self.bus, motor_controller=self.motor)
        self.handler = self.bus.subscribe.call_args.args[1]

    def tearDown(self) -> None:
        self.spine.close()

    def send(self, payload: dict) -> None:
        self.handler(MODULE.synapse_module.Impulse("MOTOR_DIRECTIVE", payload))

    def test_routes_all_supported_directives(self) -> None:
        self.send({"action": "MOVE_CURSOR", "data": {"x": 10, "y": 20}})
        self.send({"action": "CLICK_COORDS", "data": {"x": 30, "y": 40, "button": "right"}})
        self.send({"action": "TYPE_TEXT", "data": {"text": "hello", "press_enter": True}})
        self.send({"action": "HOTKEY", "data": {"keys": ["ctrl", "l"]}})

        self.motor.move_to.assert_called_once_with(10, 20)
        self.motor.natural_click.assert_called_once_with(30, 40, button="right")
        self.motor.human_type.assert_called_once_with("hello", press_enter=True)
        self.motor.hotkey_combo.assert_called_once_with("ctrl", "l")

    def test_ignores_invalid_and_unknown_directives(self) -> None:
        self.send({"action": "UNKNOWN", "data": {}})
        self.handler(MODULE.synapse_module.Impulse("MOTOR_DIRECTIVE", "invalid"))
        self.send({"action": "MOVE_CURSOR", "data": {"x": 10}})
        self.motor.assert_not_called()


if __name__ == "__main__":
    unittest.main()