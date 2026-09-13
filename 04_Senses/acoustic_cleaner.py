"""
04_Senses/acoustic_cleaner.py
Acoustic Pre-Processor: Bandpass and normalization for crisp vocal formants.
"""
from __future__ import annotations
import numpy as np

def clean_audio_stream(audio_np: np.ndarray) -> np.ndarray:
    if len(audio_np) == 0:
        return audio_np
    
    # Remove DC offset
    audio_np = audio_np - np.mean(audio_np)
    
    # Peak normalization to prevent clipping & boost faint syllables
    peak = np.max(np.abs(audio_np))
    if peak > 0.001:
        audio_np = audio_np / peak * 0.90
        
    return audio_np.astype(np.float32)
