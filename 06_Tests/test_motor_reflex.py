"""Live verification for the SynapseBus -> ReflexSpine -> HandMotor path.

Run this script manually from the repository root. It moves the real cursor
to the center of the active display.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pyautogui


ROOT_DIR = Path(__file__).parents[1]
SPINE_PATH = ROOT_DIR / "04_Spine" / "reflex_planner.py"
SPEC = importlib.util.spec_from_file_location("ultron_reflex_planner", SPINE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {SPINE_PATH}")
SPINE_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SPINE_MODULE)


def main() -> int:
    print("=== VERIFYING ULTRON MOTOR REFLEX PIPELINE ===")
    synapse = SPINE_MODULE.synapse
    if synapse is None:
        raise RuntimeError("SynapseBus could not be initialized")

    screen_width, screen_height = pyautogui.size()
    target_x, target_y = screen_width // 2, screen_height // 2
    print(f"[FIRING MOTOR IMPULSE]: Moving cursor to center ({target_x}, {target_y})...")

    futures = synapse.publish(
        "MOTOR_DIRECTIVE",
        {"action": "MOVE_CURSOR", "data": {"x": target_x, "y": target_y}},
    )
    for future in futures:
        future.result()

    current_x, current_y = pyautogui.position()
    print(f"[ACTUAL CURSOR POSITION]: ({current_x}, {current_y})")
    if abs(current_x - target_x) < 5 and abs(current_y - target_y) < 5:
        print("[SUCCESS]: Hand motor executed human Bezier trajectory accurately.")
        return 0

    print("[WARNING]: Cursor position mismatch.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())