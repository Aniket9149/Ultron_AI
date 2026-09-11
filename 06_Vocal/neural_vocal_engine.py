"""Edge-TTS synthesis and synchronous Pygame playback."""

from __future__ import annotations

import asyncio
import importlib.util
import os
from pathlib import Path
import threading
import time

import edge_tts

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame


BASE_DIR = Path(__file__).resolve().parent
AUDIO_CACHE_PATH = BASE_DIR / "ultron_speech.mp3"


def _load_phonetic_mapper() -> object | None:
    mapper_path = BASE_DIR / "phonetic_mapper.py"
    spec = importlib.util.spec_from_file_location("ultron_phonetic_mapper", mapper_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "phonetic_mapper", None)


phonetic_mapper = _load_phonetic_mapper()


class NeuralVocalEngine:
    """Synthesize mapped text and play it to completion through Pygame."""

    def __init__(
        self,
        voice: str = "hi-IN-MadhurNeural",
        pitch: str = "-4Hz",
        rate: str = "+8%",
        audio_cache_path: Path | str = AUDIO_CACHE_PATH,
    ) -> None:
        self.voice = voice
        self.pitch = pitch
        self.rate = rate
        self.audio_cache_path = Path(audio_cache_path)
        self._playback_lock = threading.Lock()
        self._init_mixer()

    def _init_mixer(self) -> None:
        try:
            pygame.mixer.quit()
        except pygame.error:
            pass
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except pygame.error:
            pass

    async def _generate_audio(self, text: str) -> None:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            pitch=self.pitch,
            rate=self.rate,
        )
        await communicate.save(str(self.audio_cache_path))

    def speak(self, text: str) -> None:
        """Synthesize and synchronously play one non-empty utterance."""
        if not text:
            return

        with self._playback_lock:
            mapper = phonetic_mapper
            tts_payload = mapper.map_for_neural_tts(text) if mapper is not None else text
            try:
                os.makedirs(self.audio_cache_path.parent, exist_ok=True)
                try:
                    self.audio_cache_path.unlink(missing_ok=True)
                except OSError as exc:
                    print(f"[NEURAL VOCAL ERROR]: Could not clear audio cache: {exc}")
                    return

                try:
                    asyncio.run(self._generate_audio(tts_payload))
                except Exception as exc:
                    print(f"[NEURAL VOCAL ERROR]: Speech synthesis failed: {exc}")
                    return

                deadline = time.monotonic() + 1.0
                while time.monotonic() < deadline:
                    if os.path.exists(self.audio_cache_path) and self.audio_cache_path.stat().st_size > 100:
                        break
                    time.sleep(0.05)
                else:
                    print("[NEURAL VOCAL ERROR]: Speech audio was not written or is empty.")
                    return

                self._init_mixer()
                pygame.mixer.music.load(str(self.audio_cache_path))
                pygame.mixer.music.play()
                clock = pygame.time.Clock()
                while pygame.mixer.music.get_busy():
                    clock.tick(30)
            except Exception as exc:  # Audio/network failures must not kill the orchestrator.
                print(f"[NEURAL VOCAL ERROR]: {exc}")
            finally:
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.quit()
                except (AttributeError, pygame.error):
                    pass
                time.sleep(0.05)


neural_vocal_engine = NeuralVocalEngine()