"""Standalone verification for the NeuralVocalEngine control flow."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "06_Vocal" / "neural_vocal_engine.py"
SPEC = importlib.util.spec_from_file_location("neural_vocal_engine", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NeuralVocalEngineTests(unittest.TestCase):
    def test_speak_maps_text_synthesizes_and_waits_for_playback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            audio_path = Path(temporary_directory) / "speech.mp3"
            mapper = MagicMock()
            mapper.map_for_neural_tts.return_value = "मुझे browser"
            clock = MagicMock()
            music = MagicMock()
            music.get_busy.side_effect = [True, False]

            async def write_audio(_: str) -> None:
                audio_path.write_bytes(b"audio" * 30)

            with patch.object(MODULE, "phonetic_mapper", mapper), \
                    patch.object(MODULE.pygame.time, "Clock", return_value=clock), \
                    patch.object(MODULE.pygame.mixer, "music", music), \
                    patch.object(MODULE.NeuralVocalEngine, "_init_mixer"), \
                    patch.object(MODULE.NeuralVocalEngine, "_generate_audio", new=AsyncMock(side_effect=write_audio)) as generate:
                engine = MODULE.NeuralVocalEngine(audio_cache_path=audio_path)
                engine.speak("Mujhe browser")

            mapper.map_for_neural_tts.assert_called_once_with("Mujhe browser")
            generate.assert_awaited_once_with("मुझे browser")
            music.load.assert_called_once_with(str(audio_path))
            music.play.assert_called_once_with()
            self.assertEqual(clock.tick.call_count, 1)
            music.unload.assert_called_once_with()

    def test_empty_text_does_not_start_synthesis(self) -> None:
        with patch.object(MODULE.NeuralVocalEngine, "_init_mixer"), \
                patch.object(MODULE.NeuralVocalEngine, "_generate_audio", new_callable=AsyncMock) as generate:
            engine = MODULE.NeuralVocalEngine()
            engine.speak("")
            generate.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()