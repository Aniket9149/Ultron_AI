"""
06_Vocal/voice_in.py
Monster Indian English Engine (Prabhat Neural)
Fixed prosody & syllable pacing - Smooth, continuous flow without word-gaps.
"""
from __future__ import annotations
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import asyncio
import tempfile
import time
from pathlib import Path
import edge_tts
import pygame

class VoiceIN:
    def __init__(self) -> None:
        self.voice_name = "en-IN-PrabhatNeural"
        # Natural continuous monster flow
        self.rate = "+6%"
        self.pitch = "-12Hz"
        if not pygame.mixer.get_init():
            pygame.mixer.init()

    async def _generate_audio(self, text: str, out_path: str) -> None:
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice_name,
            rate=self.rate,
            pitch=self.pitch
        )
        await communicate.save(out_path)

    def speak(self, text: str) -> None:
        if not text.strip():
            return

        with tempfile.NamedTemporaryFile(suffix="_monster.mp3", delete=False) as temp_f:
            temp_mp3 = temp_f.name

        try:
            asyncio.run(self._generate_audio(text, temp_mp3))

            pygame.mixer.music.load(temp_mp3)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.04)
            pygame.mixer.music.unload()

        except Exception as exc:
            print(f"[VOCAL_IN_ERROR]: {exc}")
        finally:
            try:
                Path(temp_mp3).unlink(missing_ok=True)
            except Exception:
                pass

voice_in = VoiceIN()
