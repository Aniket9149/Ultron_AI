"""
04_Senses/biometrics/enrollment_flow.py
Voice Enrollment Wizard for Ultron OS (Syntax-Safe Decoupled Importer).
"""
from __future__ import annotations
import io
import sys
import time
import wave
import numpy as np
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Safe dynamic imports for numeric folder names
ear_stream = import_module("04_Senses.ear_stream").ear_stream
voice_encoder = import_module("04_Senses.biometrics.voice_encoder").voice_encoder

PROFILE_PATH = ROOT / "01_Memory" / "user_voice_profile.npy"

PROMPTS = [
    "Ultron, systems online and standing by.",
    "I am Aniket, authorize vocal security parameters.",
    "Ultron, acknowledge my primary voice signature."
]

def run_enrollment() -> bool:
    print("=" * 60)
    print("       ULTRON OS - BIOMETRIC VOICE ENROLLMENT WIZARD       ")
    print("=" * 60)
    print("[*] Calibrating primary user voice profile...")
    print("[*] You will be asked to speak 3 standard confirmation phrases.\n")

    embeddings = []

    for idx, phrase in enumerate(PROMPTS, 1):
        input(f"Press [ENTER] when ready for Phrase {idx}/3: \"{phrase}\" ")
        print("[*] Listening... Speak clearly into your mic.")
        
        audio_bytes = ear_stream.record_phrase(max_seconds=6.0, silence_limit=1.2)
        if not audio_bytes:
            print("[!] No speech detected. Let's retry this phrase.\n")
            continue

        with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
            raw = wf.readframes(wf.getnframes())
            audio_np = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

        embed = voice_encoder.extract_embedding(audio_np)
        if np.all(embed == 0):
            print("[!] Audio sample was too short or faint. Retrying...\n")
            continue

        embeddings.append(embed)
        print(f"[+] Sample {idx}/3 captured successfully!\n")
        time.sleep(0.5)

    if len(embeddings) < 2:
        print("[-] Enrollment failed: Insufficient vocal samples.")
        return False

    master_embedding = np.mean(embeddings, axis=0)
    norm = np.linalg.norm(master_embedding)
    if norm > 0:
        master_embedding = master_embedding / norm

    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.save(str(PROFILE_PATH), master_embedding)
    print("=" * 60)
    print(f"[SUCCESS]: Voice profile locked at: {PROFILE_PATH}")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_enrollment()
