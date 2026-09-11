"""Standalone hardware-safe tests for HandMotor."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "05_Motor" / "hand_motor.py"
SPEC = importlib.util.spec_from_file_location("hand_motor", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class HandMotorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.backend = MagicMock()
        self.backend.size.return_value = (1920, 1080)
        self.backend.position.return_value = (0, 0)
        with patch.object(MODULE.time, "sleep"):
            self.motor = MODULE.HandMotor(input_backend=self.backend)

    def test_bezier_curve_has_exact_endpoints(self) -> None:
        self.assertEqual(MODULE.cubic_bezier(10, 20, 30, 40, 0), 10)
        self.assertEqual(MODULE.cubic_bezier(10, 20, 30, 40, 1), 40)

    def test_move_to_finishes_at_target_without_instant_snap(self) -> None:
        with patch.object(MODULE.time, "sleep"), patch.object(MODULE.random, "uniform", return_value=0.1), patch.object(MODULE.random, "randint", return_value=0):
            self.motor.move_to(300, 200)

        positions = [call.args for call in self.backend.moveTo.call_args_list]
        self.assertGreater(len(positions), 18)
        self.assertEqual(positions[-1], (300, 200))

    def test_click_type_and_hotkey_dispatch_to_backend(self) -> None:
        with patch.object(self.motor, "move_to") as move_to, patch.object(MODULE.time, "sleep"):
            self.motor.natural_click(30, 40, button="right")
            self.motor.human_type("ok", press_enter=True)
            self.motor.hotkey_combo("ctrl", "l")

        move_to.assert_called_once_with(30, 40)
        self.backend.mouseDown.assert_called_once_with(button="right")
        self.backend.mouseUp.assert_called_once_with(button="right")
        self.assertEqual(self.backend.write.call_args_list[0].args, ("o",))
        self.assertEqual(self.backend.write.call_args_list[1].args, ("k",))
        self.backend.press.assert_called_once_with("enter")
        self.backend.hotkey.assert_called_once_with("ctrl", "l")

    def test_scroll_dispatches_directional_wheel_steps(self) -> None:
        with patch.object(MODULE.time, "sleep"):
            self.motor.scroll("up", 4)
        self.backend.scroll.assert_called_once_with(4)


if __name__ == "__main__":
    unittest.main()