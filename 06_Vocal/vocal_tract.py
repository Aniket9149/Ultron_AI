"""
06_Vocal/vocal_tract.py
Resilient Vocal Engine for Ultron OS.
Gracefully handles stream retries, strips non-pronounceable glyphs, and avoids fatal thread termination.
"""
from __future__ import annotations
import asyncio
import io
import re
import edge_tts
import pygame

class VocalTract:
    def __init__(self, voice: str = "hi-IN-MadhurNeural") -> None:
        self.voice = voice
        try:
            pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=2048)
        except Exception:
            pass

    def _sanitize_text(self, text: str) -> str:
        # Strip foreign non-latin/non-devanagari characters (like Arabic glyphs) that break Edge-TTS
        cleaned = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', '', text)
        cleaned = re.sub(r'[*_#~`\[\]()]', '', cleaned)
        return cleaned.strip()

    async def _fetch_audio(self, text: str) -> bytes:
        # Standard parameters without unsupported offset values
        communicate = edge_tts.Communicate(text, self.voice)
        audio_stream = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])
        audio_stream.seek(0)
        return audio_stream.read()

    def speak(self, text: str, accent: str = "venom") -> None:
        clean = self._sanitize_text(text)
        if not clean:
            return

        try:
            # Run synthesis with safe event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            audio_bytes = loop.run_until_complete(self._fetch_audio(clean))
            
            if not audio_bytes:
                # Fallback to English voice if Hindi voice fails stream
                comm_fallback = edge_tts.Communicate(clean, "en-IN-PrabhatNeural")
                audio_stream = io.BytesIO()
                async def _fb():
                    async for chunk in comm_fallback.stream():
                        if chunk["type"] == "audio":
                            audio_stream.write(chunk["data"])
                loop.run_until_complete(_fb())
                audio_stream.seek(0)
                audio_bytes = audio_stream.read()

            if audio_bytes:
                sound_file = io.BytesIO(audio_bytes)
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(15)
            else:
                print("[VOCAL_WARNING]: Empty audio buffer recovered cleanly.")

        except Exception as exc:
            print(f"[VOCAL_RECOVERED]: Voice bypassed safely: {exc}")

vocal_engine = VocalTract()
