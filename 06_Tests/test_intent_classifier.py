"""Verification suite for strict TALK/TASK intent classification."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "02_Brain" / "brain_engine.py"
SPEC = importlib.util.spec_from_file_location("intent_brain_engine", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CursorRouter:
    def extract_cursor_intent(self, text: str) -> dict | None:
        if "cursor" in text and "center" in text:
            return {"action": "MOVE_CURSOR", "x": 960, "y": 540, "zone": "center"}
        return None


class IntentClassifierTests(unittest.TestCase):
    def setUp(self) -> None:
        http = MagicMock()
        http.post.return_value.status_code = 503
        self.engine = MODULE.BrainEngine(http_client=http, router=CursorRouter())

    def test_mixed_talk_and_task_inputs_have_exact_modalities(self) -> None:
        cases = [
            ("hello ultron", "TALK", "CONVERSATION"),
            ("kaisa hai bhai", "TALK", "CONVERSATION"),
            ("tum kya kar sakte ho", "TALK", "CONVERSATION"),
            ("aaj mausam kaisa hai", "TALK", "CONVERSATION"),
            ("bore ho raha hoon, shukriya", "TALK", "CONVERSATION"),
            ("brave open karo", "TASK", "OPEN_APP"),
            ("bhai sun zara ek kaam kar brave open kar", "TASK", "OPEN_APP"),
            ("new tab par click karo", "TASK", "CLICK_UI"),
            ("kya screen par koi error hai?", "TASK", "INSPECT_SCREEN"),
            ("cursor ko center mein lao", "TASK", "MOVE_CURSOR"),
            ("ctrl+w dabao", "TASK", "HOTKEY"),
            ("neeche scroll karo", "TASK", "SCROLL"),
        ]
        for text, expected_type, expected_action in cases:
            with self.subTest(text=text):
                packet = self.engine.decide(text)
                self.assertEqual(packet["type"], expected_type)
                self.assertEqual(packet["action"], expected_action)

    def test_social_preamble_is_removed_from_task_target(self) -> None:
        packet = self.engine.decide("bhai sun zara ek kaam kar brave open kar")
        self.assertEqual(packet["target"], "brave")


if __name__ == "__main__":
    unittest.main()