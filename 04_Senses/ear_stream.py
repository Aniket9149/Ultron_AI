"""
04_Senses/ear_stream.py
Calibrated Audio Streamer with Clear Visual State Logs.
"""
from __future__ import annotations
import io
import time
import wave
import pyaudio
import numpy as np

class EarStream:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024) -> None:
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.format = pyaudio.paInt16
        self.channels = 1
        self._pa = pyaudio.PyAudio()

    def record_phrase(self, max_seconds: float = 4.0, silence_limit: float = 0.8) -> bytes:
        stream = self._pa.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        frames = []
        started = False
        silence_start = None
        t0 = time.time()

        try:
            while True:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)

                chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                rms = float(np.sqrt(np.mean(chunk ** 2)))

                # Lower threshold so casual speech triggers recording easily
                if rms > 0.008:
                    if not started:
                        started = True
                        print("[MIC]: Speech detected, recording...", end="\r")
                    silence_start = None
                elif started:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > silence_limit:
                        break

                if time.time() - t0 > max_seconds:
                    break
        finally:
            stream.stop_stream()
            stream.close()

        if not started or len(frames) < 6:
            return b""

        buf = io.BytesIO()
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._pa.get_sample_size(self.format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames))

        return buf.getvalue()

ear_stream = EarStream()
