"""Standalone regression test for rapid, collision-free TTS playback."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "06_Vocal" / "neural_vocal_engine.py"
SPEC = importlib.util.spec_from_file_location("tts_robustness_engine", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TtsRobustnessTests(unittest.TestCase):
    def test_three_rapid_phrases_have_ready_audio_before_loading(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            audio_path = Path(temporary_directory) / "speech.mp3"
            music = MagicMock()
            music.get_busy.return_value = False
            clock = MagicMock()

            async def write_audio(_: str) -> None:
                audio_path.write_bytes(b"valid-mp3-placeholder" * 10)

            with patch.object(MODULE.NeuralVocalEngine, "_init_mixer"), \
                    patch.object(MODULE.NeuralVocalEngine, "_generate_audio", new=AsyncMock(side_effect=write_audio)), \
                    patch.object(MODULE.pygame.mixer, "music", music), \
                    patch.object(MODULE.pygame.time, "Clock", return_value=clock), \
                    patch.object(MODULE.time, "sleep"):
                engine = MODULE.NeuralVocalEngine(audio_cache_path=audio_path)
                for phrase in ("Pehla test.", "Doosra test.", "Teesra test."):
                    engine.speak(phrase)

            self.assertEqual(music.load.call_count, 3)
            self.assertEqual(music.play.call_count, 3)
            self.assertEqual(music.stop.call_count, 3)
            self.assertEqual(music.unload.call_count, 3)


if __name__ == "__main__":
    unittest.main()
