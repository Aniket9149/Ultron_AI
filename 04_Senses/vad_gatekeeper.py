"""
04_Senses/vad_gatekeeper.py
Adaptive Acoustic Gatekeeper for Ultron OS.
Permits conversational Hinglish while filtering empty room hiss.
"""
from __future__ import annotations
import numpy as np

class VADGatekeeper:
    def __init__(self, energy_threshold: float = 0.006, min_speech_duration: float = 0.25) -> None:
        self.energy_threshold = energy_threshold
        self.min_speech_duration = min_speech_duration

    def is_valid_speech(self, audio_np: np.ndarray, sample_rate: int = 16000) -> bool:
        if audio_np is None or len(audio_np) == 0:
            return False
        
        duration_sec = len(audio_np) / float(sample_rate)
        if duration_sec < self.min_speech_duration:
            return False

        rms = np.sqrt(np.mean(audio_np ** 2))
        return bool(rms >= self.energy_threshold)

vad_gatekeeper = VADGatekeeper()
