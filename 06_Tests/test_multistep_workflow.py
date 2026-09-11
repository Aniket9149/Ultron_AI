"""Standalone verification of two generalized multi-step desktop workflows."""

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


PLANNER = load_module("workflow_task_planner", ROOT_DIR / "02_Brain" / "task_planner.py")
EXECUTOR = load_module("workflow_execution_engine", ROOT_DIR / "03_Automation_Engines" / "execution_engine.py")
LIFE_PULSE = load_module("workflow_life_pulse", ROOT_DIR / "life_pulse.py")


class MultiStepWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        http = MagicMock()
        http.post.return_value.status_code = 503
        self.planner = PLANNER.TaskPlanner(http_client=http)
        self.operator = MagicMock()
        self.operator.open_any_app.return_value = True
        self.operator.click_element.return_value = True
        self.motor = MagicMock()
        self.inspector = MagicMock()
        self.wait = MagicMock()
        self.executor = EXECUTOR.ExecutionEngine(
            operator=self.operator,
            motor_controller=self.motor,
            inspector=self.inspector,
            wait_fn=self.wait,
        )

    def test_scenario_a_file_explorer_folder_creation(self) -> None:
        plan = self.planner.plan("File Explorer kholo aur usme Project naam ka folder banao")
        self.assertEqual([step["primitive"] for step in plan], ["LAUNCH", "WAIT", "KEYSTROKE", "KEYSTROKE"])
        self.assertEqual(plan[0]["target"], "File Explorer")
        self.assertEqual(plan[3]["text"], "Project")

        result = self.executor.execute(plan)
        self.assertTrue(result["success"])
        self.operator.open_any_app.assert_called_once_with("File Explorer")
        self.motor.hotkey_combo.assert_called_once_with("ctrl", "shift", "n")
        self.motor.human_type.assert_called_once_with("Project", True)

    def test_scenario_b_notepad_write_save_and_close(self) -> None:
        plan = self.planner.plan("Notepad kholo aur type Ultron test phrase and save and close")
        self.assertEqual(plan[0]["primitive"], "LAUNCH")
        self.assertTrue(any(step.get("action") == "TYPE" and step.get("text") == "Ultron test phrase" for step in plan))
        self.assertTrue(any(step.get("action") == "HOTKEY" and step.get("keys") == ["ctrl", "s"] for step in plan))
        self.assertTrue(any(step.get("action") == "HOTKEY" and step.get("keys") == ["alt", "f4"] for step in plan))

        result = self.executor.execute(plan)
        self.assertTrue(result["success"])
        self.operator.open_any_app.assert_called_once_with("Notepad")
        self.assertEqual(self.motor.human_type.call_count, 1)
        self.assertEqual(self.motor.hotkey_combo.call_count, 2)
        self.assertEqual(self.wait.call_count, 1)

    def test_life_pulse_routes_workflow_start_and_completion_vocally(self) -> None:
        runtime = LIFE_PULSE.RuntimeComponents(
            synapse=MagicMock(), vocals=MagicMock(), spine=MagicMock(), inspector=MagicMock(),
            operator=MagicMock(), brain=MagicMock(), wake_core=MagicMock(),
            planner=MagicMock(), executor=MagicMock(),
        )
        runtime.planner.plan.return_value = [{"step": 1, "primitive": "WAIT", "duration": 0}]
        runtime.executor.execute.return_value = {"success": True}
        LIFE_PULSE.dispatch_action(
            {"type": "TASK", "action": "MULTI_STEP_TASK", "target": "create folder", "reply": "Kaam shuru kar raha hoon."},
            runtime,
        )
        runtime.executor.execute.assert_called_once_with(runtime.planner.plan.return_value)
        vocal_messages = [call.args for call in runtime.synapse.publish.call_args_list if call.args[0] == "VOCAL_IMPULSE"]
        self.assertEqual(vocal_messages, [
            ("VOCAL_IMPULSE", {"text": "Kaam shuru kar raha hoon."}),
            ("VOCAL_IMPULSE", {"text": "Kaam poora ho gaya hai."}),
        ])


if __name__ == "__main__":
    unittest.main()
