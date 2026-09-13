"""
04_Senses/biometrics/voice_encoder.py
CPU-Thread-Throttled Biometric Encoder.
Clamps PyTorch thread hogs to eliminate Windows CPU deadlock.
"""
from __future__ import annotations
import os
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"

import torch
torch.set_num_threads(2)

import numpy as np
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy

class NeuralVoiceEncoder:
    def __init__(self, device: str = "cpu") -> None:
        self.classifier = EncoderClassifier.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="01_Memory/models/ecapa_voxceleb",
            run_opts={"device": device},
            local_strategy=LocalStrategy.COPY
        )

    @torch.inference_mode()
    def extract_embedding(self, audio_np: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
        if audio_np is None or len(audio_np) < 1600:
            return np.zeros(192, dtype=np.float32)

        try:
            tensor = torch.from_numpy(audio_np).unsqueeze(0)
            embedding = self.classifier.encode_batch(tensor)
            vector = embedding.squeeze().cpu().numpy()
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            return vector.astype(np.float32)
        except Exception:
            return np.zeros(192, dtype=np.float32)

voice_encoder = NeuralVoiceEncoder()
