"""Closed-loop state checks for desktop workflow primitives."""

from __future__ import annotations

from pathlib import Path
import time
from typing import Any, Callable


VerificationStatus = dict[str, str]


class StateVerifier:
    """Verify observable postconditions without owning any UI actuation."""

    def __init__(
        self,
        inspector: Any,
        operator: Any | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.inspector = inspector
        self.operator = operator
        self.clock = clock
        self.sleep_fn = sleep_fn

    def verify(self, step: dict[str, Any], action_succeeded: bool) -> VerificationStatus:
        """Return SUCCESS, FAILED, or TIMEOUT for one executed primitive."""
        if not action_succeeded:
            return self._status("FAILED", "Effector reported that the action was not dispatched.")

        primitive = step.get("primitive")
        if primitive == "LAUNCH":
            return self.verify_launch(str(step.get("target", "")), float(step.get("timeout", 3.0)))
        if primitive == "SHELL_EXEC":
            return self.verify_shell(step)
        if primitive == "GUI_CLICK":
            return self.verify_click(step)
        if primitive in {"KEYSTROKE", "WAIT"}:
            return self._status("SUCCESS", f"{primitive} dispatched; no stronger postcondition requested.")
        return self._status("FAILED", f"No verifier exists for primitive {primitive!r}.")

    def verify_launch(self, target: str, timeout: float = 3.0) -> VerificationStatus:
        if not target:
            return self._status("FAILED", "Launch target is empty.")
        deadline = self.clock() + max(0.0, timeout)
        last_active = "Unknown"
        last_surfaces: list[str] = []
        while True:
            active_value = self.inspector.get_active_window()
            last_active = str(active_value)
            surfaces = self.inspector.get_running_surfaces()
            if not isinstance(surfaces, (list, tuple, set)) or not isinstance(active_value, str):
                return self._status("SUCCESS", "Launch dispatched; surface observation is unavailable.")
            last_surfaces = [str(surface) for surface in surfaces]
            target_folded = target.casefold()
            focused = target_folded in last_active.casefold()
            has_window = focused or any(target_folded in surface.casefold() for surface in last_surfaces)
            if has_window and focused:
                return self._status("SUCCESS", f"'{target}' is running and focused.")
            if self.clock() >= deadline:
                break
            self.sleep_fn(min(0.1, max(0.0, deadline - self.clock())))
        return self._status(
            "TIMEOUT",
            f"'{target}' was not focused; active={last_active!r}, surfaces={last_surfaces!r}.",
        )

    def verify_shell(self, step: dict[str, Any]) -> VerificationStatus:
        expected_path = step.get("expected_path", step.get("path"))
        if not expected_path:
            return self._status("SUCCESS", "Shell command completed; no filesystem postcondition requested.")
        path = Path(str(expected_path)).expanduser()
        should_exist = bool(step.get("should_exist", True))
        exists = path.exists()
        if exists == should_exist:
            return self._status("SUCCESS", f"Filesystem state verified for {path}.")
        return self._status("FAILED", f"Expected exists={should_exist} for {path}, observed {exists}.")

    def verify_click(self, step: dict[str, Any]) -> VerificationStatus:
        expected = step.get("expected_element")
        if expected and self.operator is not None:
            grounding = getattr(self.operator, "ui_grounding", None)
            locator = getattr(grounding, "locate_active_text", None)
            if callable(locator) and locator(str(expected)):
                return self._status("SUCCESS", f"Expected UI element '{expected}' is present.")
            return self._status("FAILED", f"Expected UI element '{expected}' was not found after click.")

        if step.get("expected_disappear") and self.operator is not None:
            grounding = getattr(self.operator, "ui_grounding", None)
            locator = getattr(grounding, "locate_active_text", None)
            if callable(locator) and not locator(str(step.get("target", ""))):
                return self._status("SUCCESS", "Clicked element disappeared as expected.")
            return self._status("TIMEOUT", "Clicked element is still present.")

        return self._status("SUCCESS", "Click dispatched; no explicit UI postcondition requested.")

    @staticmethod
    def _status(status: str, details: str) -> VerificationStatus:
        return {"status": status, "details": details}


verifier = None