"""Standalone tests for BrainEngine reflex, LLM, and fallback paths."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "02_Brain" / "brain_engine.py"
SPEC = importlib.util.spec_from_file_location("brain_engine", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BrainEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.http = MagicMock()
        self.router = MagicMock()
        self.engine = MODULE.BrainEngine(http_client=self.http, router=self.router)

    def test_screen_and_cursor_reflexes_skip_llm(self) -> None:
        self.assertEqual(self.engine.decide("screen par kya dikh raha hai")["action"], "INSPECT_SCREEN")
        self.router.extract_cursor_intent.assert_not_called()
        self.http.post.assert_not_called()

        self.router.extract_cursor_intent.return_value = {
            "action": "MOVE_CURSOR", "x": 10, "y": 20, "zone": "left"
        }
        packet = self.engine.decide("pointer left move karo")
        self.assertEqual(packet["zone"], "left")
        self.http.post.assert_not_called()

    def test_parses_raw_json_from_lm_studio(self) -> None:
        response = MagicMock(status_code=200)
        response.json.return_value = {
            "choices": [{"message": {"content": '```json {"action":"CHAT","response":"hello"} ```'}}]
        }
        self.http.post.return_value = response
        self.router.extract_cursor_intent.return_value = None

        packet = self.engine.decide("hello")
        self.assertEqual(packet["type"], "TALK")
        self.assertEqual(packet["action"], "CONVERSATION")
        self.http.post.assert_called_once()

    def test_extracts_click_target_without_calling_lm(self) -> None:
        self.router.extract_cursor_intent.return_value = None
        packet = self.engine.decide("New tab par click karo")
        self.assertEqual(packet["action"], "CLICK_UI")
        self.assertEqual(packet["target"], "new tab")
        self.http.post.assert_not_called()

    def test_falls_back_when_lm_studio_is_unavailable(self) -> None:
        self.http.post.side_effect = MODULE.requests.RequestException("offline")
        self.router.extract_cursor_intent.return_value = None
        packet = self.engine.decide("open calculator")
        self.assertEqual(packet["action"], "OPEN_APP")
        self.assertEqual(packet["target"], "calculator")


if __name__ == "__main__":
    unittest.main()