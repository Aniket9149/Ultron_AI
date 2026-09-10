"""Translate motor directives from the SynapseBus into HandMotor actions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from typing import Any, Callable


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


def _load_module(module_name: str, path: Path) -> Any | None:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


synapse_module = _load_module("ultron_spine_synapse_bus", ROOT_DIR / "02_Nerves" / "synapse_bus.py")
motor_module = _load_module("ultron_spine_hand_motor", ROOT_DIR / "05_Motor" / "hand_motor.py")
synapse = synapse_module.SynapseBus() if synapse_module is not None else None
motor = getattr(motor_module, "hand_motor", None)


DirectiveHandler = Callable[[dict[str, Any]], None]


class ReflexSpine:
    """Route validated motor directives to the physical motor abstraction."""

    def __init__(self, bus: Any | None = None, motor_controller: Any | None = None) -> None:
        self._bus = bus if bus is not None else synapse
        self._motor = motor_controller if motor_controller is not None else motor
        self._subscription = None
        self._handlers: dict[str, DirectiveHandler] = {
            "MOVE_CURSOR": self._move_cursor,
            "CLICK_COORDS": self._click_coords,
            "TYPE_TEXT": self._type_text,
            "HOTKEY": self._hotkey,
        }
        if self._bus is not None:
            self._subscription = self._bus.subscribe("MOTOR_DIRECTIVE", self._execute_directive)

    def close(self) -> None:
        """Detach the planner from the event bus."""
        if self._subscription is not None:
            self._subscription.cancel()
            self._subscription = None

    def _execute_directive(self, impulse: Any) -> None:
        if self._motor is None:
            return
        payload = getattr(impulse, "payload", impulse)
        if not isinstance(payload, dict):
            return
        action = payload.get("action")
        data = payload.get("data", {})
        if not isinstance(action, str) or not isinstance(data, dict):
            return
        handler = self._handlers.get(action.strip().upper())
        if handler is not None:
            handler(data)

    def _move_cursor(self, data: dict[str, Any]) -> None:
        x, y = data.get("x"), data.get("y")
        if x is not None and y is not None:
            self._motor.move_to(x, y)

    def _click_coords(self, data: dict[str, Any]) -> None:
        x, y = data.get("x"), data.get("y")
        if x is not None and y is not None:
            self._motor.natural_click(x, y, button=data.get("button", "left"))

    def _type_text(self, data: dict[str, Any]) -> None:
        self._motor.human_type(data.get("text", ""), press_enter=data.get("press_enter", False))

    def _hotkey(self, data: dict[str, Any]) -> None:
        keys = data.get("keys", [])
        if isinstance(keys, (list, tuple)) and keys:
            self._motor.hotkey_combo(*keys)


reflex_spine = ReflexSpine()