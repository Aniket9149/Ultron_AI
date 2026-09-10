"""Resolve relative cursor intents into screen coordinates."""

from __future__ import annotations

from typing import Any

import pyautogui


POINTER_TRIGGERS = ("pointer", "mouse", "cursor")
MOVE_TRIGGERS = ("lao", "le jao", "le aao", "rakho", "move", "karo", "shift")
ZONE_TRIGGERS = {
    "center": ("center", "centre", "bich", "beech"),
    "left": ("left", "baye"),
    "right": ("right", "daye"),
    "top": ("top", "upar"),
    "bottom": ("bottom", "neeche"),
}


def _contains_trigger(text: str, triggers: tuple[str, ...]) -> bool:
    return any(trigger in text for trigger in triggers)


def extract_cursor_intent(text: str, screen_api: Any = pyautogui) -> dict[str, Any] | None:
    """Return a motor-ready relative cursor directive, or ``None``."""
    if not isinstance(text, str):
        return None

    normalized = text.casefold()
    if not _contains_trigger(normalized, POINTER_TRIGGERS) or not _contains_trigger(
        normalized, MOVE_TRIGGERS
    ):
        return None

    width, height = screen_api.size()
    zone_coordinates = {
        "center": (width // 2, height // 2),
        "left": (int(width * 0.15), height // 2),
        "right": (int(width * 0.85), height // 2),
        "top": (width // 2, int(height * 0.15)),
        "bottom": (width // 2, int(height * 0.85)),
    }

    for zone, triggers in ZONE_TRIGGERS.items():
        if _contains_trigger(normalized, triggers):
            x, y = zone_coordinates[zone]
            return {"action": "MOVE_CURSOR", "x": x, "y": y, "zone": zone}
    return None