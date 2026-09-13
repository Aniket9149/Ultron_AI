"""
main_loop.py
Ultron OS - Autonomous Execution Loop.
Direct speech-to-action sovereign engine.
"""
from __future__ import annotations
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
import time
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ear_stream = import_module("04_Senses.ear_stream").ear_stream
speech_cortex = import_module("04_Senses.speech_cortex").speech_cortex
generate_and_execute = import_module("03_Brain.qwen_generator").generate_and_execute
vocal_engine = import_module("06_Vocal.vocal_tract").vocal_engine

def run_ultron():
    print("=" * 60)
    print("[*] ULTRON ACTIVE - Autonomous System Control | User: Aniket")
    print("=" * 60)

    boot = "Ultron online. Pura system mere control me hai. Bol kya tod-phod karni hai?"
    print(f"\n[ULTRON]: {boot}\n")
    vocal_engine.speak(boot)

    while True:
        try:
            print("[*] Listening...")
            audio_bytes = ear_stream.record_phrase(max_seconds=4.0, silence_limit=0.7)
            if not audio_bytes:
                continue

            user_text = speech_cortex.transcribe(audio_bytes)
            if not user_text:
                continue

            print(f"[Aniket]: \"{user_text}\"")
            
            t0 = time.time()
            reply = generate_and_execute(user_text)
            print(f"[GENERATOR]: {round(time.time() - t0, 2)}s")
            print(f"[Ultron]: {reply}\n")

            vocal_engine.speak(reply)

        except KeyboardInterrupt:
            print("\n[*] Ultron shutting down.")
            break
        except Exception as exc:
            print(f"[MAIN_ERROR]: {exc}")
            time.sleep(0.5)

if __name__ == "__main__":
    run_ultron()
