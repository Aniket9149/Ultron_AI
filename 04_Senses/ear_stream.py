"""
04_Senses/ear_stream.py
Low-Latency Audio Capture & Silence Truncator.
Captures user audio via microphone and buffers speech chunks.
"""
from __future__ import annotations
import numpy as np
import sounddevice as sd
import queue
import io
import wave

class EarStream:
    def __init__(self, sample_rate: int = 16000, threshold: float = 0.015) -> None:
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.audio_queue = queue.Queue()
        self.is_listening = False

    def _callback(self, indata, frames, time_info, status):
        if status:
            pass
        self.audio_queue.put(indata.copy())

    def record_phrase(self, max_seconds: int = 8, silence_limit: float = 1.2) -> bytes | None:
        """
        Records microphone audio until silence is detected or max duration is hit.
        Returns PCM WAV bytes.
        """
        print("\n[*] Listening... (speak now)")
        self.audio_queue.queue.clear()
        
        audio_buffer = []
        has_spoken = False
        silence_frames = 0
        silence_threshold_frames = int((self.sample_rate / 1024) * silence_limit)

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32",
                            blocksize=1024, callback=self._callback):
            while True:
                chunk = self.audio_queue.get()
                amplitude = np.max(np.abs(chunk))

                if amplitude > self.threshold:
                    has_spoken = True
                    silence_frames = 0
                elif has_spoken:
                    silence_frames += 1

                if has_spoken:
                    audio_buffer.append(chunk)

                # Stop if silence threshold reached after speech
                if has_spoken and silence_frames > silence_threshold_frames:
                    break

                # Safety cap
                if len(audio_buffer) * 1024 / self.sample_rate > max_seconds:
                    break

        if not audio_buffer:
            print("[*] No speech detected.")
            return None

        # Concatenate & convert to 16-bit PCM WAV
        full_audio = np.concatenate(audio_buffer, axis=0)
        pcm16 = (full_audio * 32767).astype(np.int16)

        wav_io = io.BytesIO()
        with wave.open(wav_io, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(pcm16.tobytes())

        return wav_io.getvalue()

ear_stream = EarStream()
