"""Standalone tests for wake-word recognition without a microphone."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock


MODULE_PATH = Path(__file__).parents[1] / "01_Voice" / "wake_detector.py"
SPEC = importlib.util.spec_from_file_location("wake_detector", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WakeDetectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.detector = MODULE.UltronWakeDetector()
        self.recognizer = MagicMock()
        self.detector.recognizer = self.recognizer

    def test_detects_supported_wake_word(self) -> None:
        self.recognizer.listen.return_value = object()
        self.recognizer.recognize_google.return_value = "Hey Ultron, are you there?"

        self.assertTrue(self.detector.listen_for_wake_word(MagicMock()))
        self.recognizer.listen.assert_called_once_with(
            unittest.mock.ANY,
            timeout=None,
            phrase_time_limit=3.0,
        )
        self.recognizer.recognize_google.assert_called_once_with(
            unittest.mock.ANY,
            language="en-IN",
        )

    def test_ignores_unknown_speech_and_non_matching_text(self) -> None:
        self.recognizer.listen.return_value = object()
        self.recognizer.recognize_google.return_value = "hello computer"
        self.assertFalse(self.detector.listen_for_wake_word(MagicMock()))

        self.recognizer.recognize_google.side_effect = MODULE.sr.UnknownValueError()
        self.assertFalse(self.detector.listen_for_wake_word(MagicMock()))


if __name__ == "__main__":
    unittest.main()