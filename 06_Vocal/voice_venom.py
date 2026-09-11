"""
06_Vocal/voice_venom.py
Deep Authoritative Monster Voice (Native Neural Delivery):
- Pure 100% word clarity with zero audio-file distortion
- Native deep pitch (-15Hz) for heavy presence
- Snappy tempo (+6%) to avoid sluggish, dragging speech
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

class VenomVocalEngine:
    def __init__(self) -> None:
        self.voice_name = "en-IN-PrabhatNeural"
        # Pure vocal clarity settings: deep commanding baritone, zero muffle
        self.rate = "+6%"
        self.pitch = "-15Hz"
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

        with tempfile.NamedTemporaryFile(suffix="_venom.mp3", delete=False) as temp_f:
            temp_mp3 = temp_f.name

        try:
            asyncio.run(self._generate_audio(text, temp_mp3))

            pygame.mixer.music.load(temp_mp3)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.03)
            pygame.mixer.music.unload()

        except Exception as exc:
            print(f"[VENOM_ERROR]: {exc}")
        finally:
            try:
                Path(temp_mp3).unlink(missing_ok=True)
            except Exception:
                pass

voice_venom = VenomVocalEngine()
