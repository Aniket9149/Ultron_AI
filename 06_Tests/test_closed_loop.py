"""Standalone verification of bounded desktop self-correction."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock


ROOT_DIR = Path(__file__).parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


EXECUTOR = load_module("closed_loop_execution_engine", ROOT_DIR / "03_Automation_Engines" / "execution_engine.py")


class ClosedLoopWorkflowTests(unittest.TestCase):
    def test_missing_button_retries_rescans_and_uses_hotkey_fallback(self) -> None:
        operator = MagicMock()
        operator.click_element.return_value = False
        motor = MagicMock()
        inspector = MagicMock()
        bus = MagicMock()
        engine = EXECUTOR.ExecutionEngine(
            operator=operator,
            motor_controller=motor,
            inspector=inspector,
            bus=bus,
            max_corrections=2,
        )

        result = engine.execute([
            {
                "step": 1,
                "primitive": "GUI_CLICK",
                "target": "New Tab",
            }
        ])

        self.assertFalse(result["success"])
        self.assertEqual(result["failed_step"], 1)
        self.assertEqual(operator.click_element.call_count, 4)
        motor.hotkey_combo.assert_called_once_with("ctrl", "t")
        vocal_messages = [
            call.args[1]["text"]
            for call in bus.publish.call_args_list
            if call.args[0] == "VOCAL_IMPULSE"
        ]
        self.assertEqual(vocal_messages[0], "UI ko dobara scan kar raha hoon...")
        self.assertEqual(vocal_messages[1], "Click miss hua, shortcut try kar raha hoon...")
        self.assertIn("Effector reported", vocal_messages[-1])


if __name__ == "__main__":
    unittest.main()
