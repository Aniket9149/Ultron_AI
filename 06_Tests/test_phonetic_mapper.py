"""Standalone verification for the phonetic mapper."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "06_Vocal" / "phonetic_mapper.py"
SPEC = importlib.util.spec_from_file_location("phonetic_mapper", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["phonetic_mapper"] = MODULE
SPEC.loader.exec_module(MODULE)


class PhoneticMapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mapper = MODULE.PhoneticMapper()

    def test_maps_hinglish_and_preserves_technical_terms(self) -> None:
        result = self.mapper.map_for_neural_tts("Mujhe browser open karo, Ultron!")
        self.assertEqual(result, "मुझे browser open करो, Ultron!")

    def test_removes_breath_traps_and_normalizes_punctuation(self) -> None:
        result = self.mapper.map_for_neural_tts("main...  kya__ karu??")
        self.assertEqual(result, "मैं क्या karu??")

    def test_empty_input_is_safe(self) -> None:
        self.assertEqual(self.mapper.map_for_neural_tts(""), "")


if __name__ == "__main__":
    unittest.main()