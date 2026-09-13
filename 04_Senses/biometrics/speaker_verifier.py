"""
04_Senses/biometrics/speaker_verifier.py
Tuned Biometric Audio Gate.
Calibrated threshold (0.35) to prevent accidental drops on casual speech.
"""
from __future__ import annotations
import sys
import numpy as np
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PROFILE_PATH = ROOT / "01_Memory" / "user_voice_profile.npy"

class SpeakerVerifier:
    def __init__(self, threshold: float = 0.35) -> None:
        self.threshold = threshold
        self.master_profile: np.ndarray | None = None
        self.encoder = import_module("04_Senses.biometrics.voice_encoder").voice_encoder
        self.reload_profile()

    def reload_profile(self) -> bool:
        if PROFILE_PATH.exists():
            try:
                self.master_profile = np.load(str(PROFILE_PATH))
                return True
            except Exception:
                self.master_profile = None
        return False

    def is_enrolled(self) -> bool:
        return self.master_profile is not None

    def verify_speaker(self, audio_np: np.ndarray, sample_rate: int = 16000) -> tuple[bool, float]:
        if not self.is_enrolled():
            return True, 1.0

        rms = np.sqrt(np.mean(audio_np ** 2))
        if rms < 0.008:
            return False, 0.0

        embed = self.encoder.extract_embedding(audio_np, sample_rate=sample_rate)
        if np.all(embed == 0):
            return False, 0.0

        norm_e = np.linalg.norm(embed)
        if norm_e > 0:
            embed = embed / norm_e

        similarity = float(np.dot(self.master_profile, embed))
        is_match = bool(similarity >= self.threshold)
        return is_match, round(similarity, 3)

speaker_verifier = SpeakerVerifier()
