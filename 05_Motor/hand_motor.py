"""Human-like mouse and keyboard actuation primitives."""

from __future__ import annotations

import math
import random
import time
from typing import Any

import pyautogui


pyautogui.FAILSAFE = True


def cubic_bezier(p0: float, p1: float, p2: float, p3: float, t: float) -> float:
    """Calculate one coordinate on a cubic Bezier curve."""
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


class HandMotor:
    """Dispatch gradual pointer and keyboard actions through PyAutoGUI."""

    def __init__(self, input_backend: Any = pyautogui) -> None:
        self.input_backend = input_backend
        self.screen_w, self.screen_h = input_backend.size()

    def move_to(self, target_x: int, target_y: int, speed: float = 0.45) -> None:
        """Move the cursor along an eased, randomized Bezier path."""
        start_x, start_y = self.input_backend.position()
        distance = math.hypot(target_x - start_x, target_y - start_y)

        if distance < 8:
            self.input_backend.moveTo(target_x, target_y)
            return

        arc_strength = random.uniform(0.15, 0.30)
        ctrl_x1 = start_x + (target_x - start_x) * 0.3 + random.uniform(
            -distance * arc_strength, distance * arc_strength
        )
        ctrl_y1 = start_y + (target_y - start_y) * 0.3 + random.uniform(
            -distance * arc_strength, distance * arc_strength
        )
        ctrl_x2 = start_x + (target_x - start_x) * 0.7 + random.uniform(
            -distance * arc_strength, distance * arc_strength
        )
        ctrl_y2 = start_y + (target_y - start_y) * 0.7 + random.uniform(
            -distance * arc_strength, distance * arc_strength
        )

        steps = max(18, int(distance / 30))
        duration = speed + random.uniform(0.04, 0.12)
        step_sleep = duration / steps

        for step in range(steps + 1):
            t = step / float(steps)
            eased_t = t * t * (3 - 2 * t)
            next_x = cubic_bezier(start_x, ctrl_x1, ctrl_x2, target_x, eased_t)
            next_y = cubic_bezier(start_y, ctrl_y1, ctrl_y2, target_y, eased_t)

            if 4 < step < steps - 4:
                next_x += random.randint(-1, 1)
                next_y += random.randint(-1, 1)

            self.input_backend.moveTo(int(next_x), int(next_y))
            time.sleep(step_sleep)

        self.input_backend.moveTo(target_x, target_y)
        time.sleep(random.uniform(0.05, 0.10))

    def natural_click(
        self,
        x: int | None = None,
        y: int | None = None,
        button: str = "left",
    ) -> None:
        """Perform a humanized mouse click, optionally moving first."""
        if x is not None and y is not None:
            self.move_to(x, y)
        time.sleep(random.uniform(0.03, 0.06))
        self.input_backend.mouseDown(button=button)
        time.sleep(random.uniform(0.06, 0.10))
        self.input_backend.mouseUp(button=button)
        time.sleep(0.05)

    def human_type(self, text: str, press_enter: bool = False) -> None:
        """Type text with randomized micro-intervals between characters."""
        for character in text:
            self.input_backend.write(character)
            time.sleep(random.uniform(0.02, 0.05))
        if press_enter:
            time.sleep(0.08)
            self.input_backend.press("enter")

    def hotkey_combo(self, *keys: str) -> None:
        """Dispatch a physical key combination."""
        self.input_backend.hotkey(*keys)
        time.sleep(0.12)

    def scroll(self, direction: str = "down", amount: int = 3) -> None:
        """Scroll a small, deliberate number of wheel steps."""
        clicks = abs(int(amount))
        self.input_backend.scroll(clicks if direction.casefold() == "up" else -clicks)
        time.sleep(0.12)


hand_motor = HandMotor()