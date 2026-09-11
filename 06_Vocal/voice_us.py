"""
06_Vocal/voice_us.py
Dedicated US Accent Engine (Microsoft David / US English Male + Cyber DSP)
"""
from __future__ import annotations
import math
import struct
import tempfile
import wave
from pathlib import Path
import winsound
import comtypes.client

class VoiceUS:
    def __init__(self) -> None:
        self._voice = comtypes.client.CreateObject("SAPI.SpVoice")
        self._file_stream = comtypes.client.CreateObject("SAPI.SpFileStream")
        
        voices = self._voice.GetVoices()
        for i in range(voices.Count):
            v = voices.Item(i)
            desc = v.GetDescription().lower()
            if "united kingdom" in desc or "george" in desc:
                continue
            if "david" in desc or "en-us" in desc:
                self._voice.Voice = v
                break

        self._voice.Rate = 1
        self._voice.Volume = 100

    def _apply_dsp(self, in_path: str, out_path: str) -> None:
        with wave.open(in_path, "rb") as wf:
            params = wf.getparams()
            frames = wf.readframes(wf.getnframes())

        count = len(frames) // 2
        samples = list(struct.unpack(f"<{count}h", frames))
        sample_rate = params.framerate or 22050

        processed = []
        for i, s in enumerate(samples):
            norm = s / 32768.0
            t = i / sample_rate
            ring_mod = 0.58 + 0.32 * math.sin(2 * math.pi * 125.0 * t) + 0.10 * math.sin(2 * math.pi * 250.0 * t)
            cyber = math.tanh((norm * ring_mod) * 1.75)
            blended = (norm * 0.68) + (cyber * 0.40)
            val = max(-32768, min(32767, int(blended * 32767.0)))
            processed.append(val)

        with wave.open(out_path, "wb") as out_wf:
            out_wf.setparams(params)
            out_wf.writeframes(struct.pack(f"<{count}h", *processed))

    def speak(self, text: str) -> None:
        if not text.strip():
            return
        with tempfile.NamedTemporaryFile(suffix="_us_raw.wav", delete=False) as raw_f, \
             tempfile.NamedTemporaryFile(suffix="_us_dsp.wav", delete=False) as dsp_f:
            raw_wav = raw_f.name
            dsp_wav = dsp_f.name
        try:
            self._file_stream.Open(raw_wav, 3, False)
            self._voice.AudioOutputStream = self._file_stream
            self._voice.Speak(text)
            self._file_stream.Close()
            self._voice.AudioOutputStream = None
            self._apply_dsp(raw_wav, dsp_wav)
            winsound.PlaySound(dsp_wav, winsound.SND_FILENAME)
        finally:
            for p in (raw_wav, dsp_wav):
                try:
                    Path(p).unlink(missing_ok=True)
                except Exception:
                    pass

voice_us = VoiceUS()
