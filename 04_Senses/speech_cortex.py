"""
04_Senses/speech_cortex.py
Upgraded to 'small' model for robust Indian accent & Hindi comprehension.
"""
from __future__ import annotations
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
os.environ["CT2_NUM_THREADS"] = "4"

import io
import re
import sys
import wave
import time
import numpy as np
from pathlib import Path
from importlib import import_module
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

verifier = import_module("04_Senses.biometrics.speaker_verifier").speaker_verifier

class SpeechCortex:
    def __init__(self, model_size: str = "small", device: str = "cpu", compute_type: str = "int8") -> None:
        print(f"[*] Initializing Robust Hindi/Hinglish Cortex ({model_size})...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type, cpu_threads=4)

    def transcribe(self, audio_data: bytes) -> str:
        if not audio_data or len(audio_data) < 2000:
            return ""

        t0 = time.time()
        try:
            with wave.open(io.BytesIO(audio_data), "rb") as wf:
                raw_bytes = wf.readframes(wf.getnframes())
                audio_np = np.frombuffer(raw_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            # 1. Biometric Check
            is_match, score = verifier.verify_speaker(audio_np)
            if score == 0.0 or not is_match:
                if score > 0.0:
                    print(f"[GATE]: Ignored (Score: {score} < {verifier.threshold})")
                return ""

            print(f"[GATE]: Verified ({score}) -> Transcribing with Small Model...")

            # 2. Transcribe using Hindi acoustic priors
            segments, _ = self.model.transcribe(
                audio_np,
                language="hi",
                beam_size=2,
                temperature=0.0,
                condition_on_previous_text=False,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=250, threshold=0.4)
            )

            raw_text = " ".join([seg.text for seg in segments]).strip()

            # Normalization
            clean = re.sub(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+', '', raw_text)
            clean = re.sub(r'(?i)\b(ओल्ट्रॉन|वेलड्रोन|अल्ट्रॉन|altron|veltron|all turn)\b', 'Ultron', clean)
            clean = " ".join(clean.split())

            if not clean:
                return ""

            print(f"[CORTEX]: Transcribed in {round(time.time() - t0, 2)}s -> \"{clean}\"")
            return clean

        except Exception as exc:
            print(f"[CORTEX_ERROR]: {exc}")
            return ""

speech_cortex = SpeechCortex()
