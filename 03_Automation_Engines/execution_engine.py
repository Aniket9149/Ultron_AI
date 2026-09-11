"""Sequential executor for generalized atomic desktop workflow steps."""

from __future__ import annotations

import shlex
import subprocess
import time
import importlib.util
from pathlib import Path
import sys
from typing import Any, Callable

try:
    from verifier import StateVerifier
except ModuleNotFoundError:
    verifier_path = Path(__file__).with_name("verifier.py")
    verifier_spec = importlib.util.spec_from_file_location("ultron_state_verifier", verifier_path)
    if verifier_spec is None or verifier_spec.loader is None:
        raise ImportError(f"Unable to load {verifier_path}")
    verifier_module = importlib.util.module_from_spec(verifier_spec)
    sys.modules["ultron_state_verifier"] = verifier_module
    verifier_spec.loader.exec_module(verifier_module)
    StateVerifier = verifier_module.StateVerifier


class WorkflowExecutionError(RuntimeError):
    """Raised when a workflow step cannot complete safely."""


class ExecutionEngine:
    """Route validated primitives to OS, UI, keyboard, and wait effectors."""

    SAFE_SHELL_COMMANDS = {"get-childitem", "get-content", "new-item", "test-path", "copy-item", "move-item"}

    def __init__(
        self,
        operator: Any,
        motor_controller: Any,
        inspector: Any,
        shell_runner: Callable[..., Any] | None = None,
        wait_fn: Callable[[float], None] = time.sleep,
        verifier: StateVerifier | None = None,
        bus: Any | None = None,
        max_corrections: int = 2,
    ) -> None:
        self.operator = operator
        self.motor = motor_controller
        self.inspector = inspector
        self.shell_runner = shell_runner or subprocess.run
        self.wait_fn = wait_fn
        self.verifier = verifier or StateVerifier(inspector, operator, sleep_fn=wait_fn)
        self.bus = bus
        self.max_corrections = max(0, max_corrections)

    def execute(self, plan: list[dict[str, Any]]) -> dict[str, Any]:
        """Execute steps in order and stop at the first failed step."""
        completed: list[int] = []
        diagnostics: list[dict[str, Any]] = []
        for index, step in enumerate(plan, start=1):
            step_number = step.get("step", index)
            try:
                result = self._execute_with_correction(step)
                diagnostics.append({"step": step_number, **result["verification"]})
                if not result["success"]:
                    return {
                        "success": False,
                        "completed": completed,
                        "failed_step": step_number,
                        "verification": diagnostics,
                        "error": result["verification"]["details"],
                    }
                completed.append(step_number)
            except Exception as exc:
                return {
                    "success": False,
                    "completed": completed,
                    "failed_step": step_number,
                    "error": str(exc),
                    "verification": diagnostics,
                }
        return {"success": True, "completed": completed, "verification": diagnostics}

    def _execute_with_correction(self, step: dict[str, Any]) -> dict[str, Any]:
        corrections = 0
        while True:
            dispatched = self._execute_step(step)
            verification = self.verifier.verify(step, dispatched)
            if verification["status"] == "SUCCESS":
                return {"success": True, "verification": verification}
            if corrections >= self.max_corrections:
                self._announce(f"Kaam ruk gaya: {verification['details']}")
                return {"success": False, "verification": verification}
            corrections += 1
            self._announce(self._correction_message(step, corrections))
            self._correct(step, corrections)

    def _correct(self, step: dict[str, Any], attempt: int) -> None:
        primitive = step.get("primitive")
        if primitive == "GUI_CLICK":
            if attempt == 1:
                # A second call re-grounds against the current UIA tree.
                self.operator.click_element(str(step.get("target", "")))
            elif attempt == 2:
                fallback = step.get("fallback_keys")
                if not fallback and "tab" in str(step.get("target", "")).casefold():
                    fallback = ["ctrl", "t"]
                if fallback:
                    self.motor.hotkey_combo(*fallback)
        elif primitive == "LAUNCH" and attempt == 2:
            self.operator.open_any_app(str(step.get("target", "")))
        elif primitive == "KEYSTROKE" and attempt == 1:
            self._verify_window(step)

    @staticmethod
    def _correction_message(step: dict[str, Any], attempt: int) -> str:
        if step.get("primitive") == "GUI_CLICK":
            return "Click miss hua, shortcut try kar raha hoon..." if attempt == 2 else "UI ko dobara scan kar raha hoon..."
        return "Action verify nahi hua, dobara try kar raha hoon..."

    def _announce(self, text: str) -> None:
        if self.bus is not None:
            self.bus.publish("VOCAL_IMPULSE", {"text": text})

    def _execute_step(self, step: dict[str, Any]) -> bool:
        primitive = step.get("primitive")
        if primitive == "LAUNCH":
            return bool(self.operator.open_any_app(str(step.get("target", ""))))
        if primitive == "SHELL_EXEC":
            return self._execute_shell(step)
        if primitive == "GUI_CLICK":
            return bool(self.operator.click_element(str(step.get("target", ""))))
        if primitive == "KEYSTROKE":
            self._verify_window(step)
            return self._execute_keystroke(step)
        if primitive == "WAIT":
            self.wait_fn(max(0.0, float(step.get("duration", 0.0))))
            return True
        raise WorkflowExecutionError(f"Unsupported workflow primitive: {primitive!r}")

    def _verify_window(self, step: dict[str, Any]) -> None:
        expected = step.get("expected_window")
        if not expected:
            return
        active = self.inspector.get_active_window()
        if expected.casefold() not in active.casefold():
            raise WorkflowExecutionError(f"Expected window {expected!r}, active window is {active!r}")

    def _execute_keystroke(self, step: dict[str, Any]) -> bool:
        action = str(step.get("action", "")).upper()
        if action == "TYPE":
            self.motor.human_type(str(step.get("text", "")), bool(step.get("press_enter", False)))
            return True
        if action == "HOTKEY":
            keys = step.get("keys", [])
            if not isinstance(keys, (list, tuple)) or not keys:
                return False
            self.motor.hotkey_combo(*keys)
            return True
        if action == "PRESS":
            self.motor.human_type("", press_enter=str(step.get("key", "")).casefold() == "enter")
            return True
        return False

    def _execute_shell(self, step: dict[str, Any]) -> bool:
        command = step.get("command")
        if isinstance(command, str):
            command = shlex.split(command, posix=False)
        if not isinstance(command, (list, tuple)) or not command:
            return False
        command = [str(part) for part in command]
        self._validate_shell_command(command)
        result = self.shell_runner(command, capture_output=True, text=True, timeout=float(step.get("timeout", 30)))
        if getattr(result, "returncode", 1) != 0:
            raise WorkflowExecutionError(getattr(result, "stderr", "Shell command failed"))
        return True

    def _validate_shell_command(self, command: list[str]) -> None:
        executable = command[0].casefold().rsplit("\\", 1)[-1]
        if executable in ("powershell", "powershell.exe", "pwsh", "pwsh.exe"):
            try:
                script = command[command.index("-Command") + 1].strip()
            except (ValueError, IndexError):
                raise WorkflowExecutionError("PowerShell command must include -Command")
            verb = script.split(maxsplit=1)[0].casefold()
            if verb not in self.SAFE_SHELL_COMMANDS:
                raise WorkflowExecutionError(f"PowerShell verb is not allowlisted: {verb!r}")
        elif executable not in self.SAFE_SHELL_COMMANDS:
            raise WorkflowExecutionError(f"Shell executable is not allowlisted: {executable!r}")


execution_engine = None
