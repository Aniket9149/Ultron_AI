"""
04_Senses/wake_warden.py
Zero-cost wake-word trigger engine for Ultron OS.
Continuously scans ambient speech for the wake trigger.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Dynamic module loaders
e_spec = importlib.util.spec_from_file_location("ear_stream", ROOT / "04_Senses" / "ear_stream.py")
e_mod = importlib.util.module_from_spec(e_spec)
e_spec.loader.exec_module(e_mod)
ear = e_mod.ear_stream

s_spec = importlib.util.spec_from_file_location("speech_cortex", ROOT / "04_Senses" / "speech_cortex.py")
s_mod = importlib.util.module_from_spec(s_spec)
s_spec.loader.exec_module(s_mod)
cortex = s_mod.speech_cortex

class WakeWarden:
    def __init__(self, trigger_word: str = "ultron") -> None:
        self.trigger_word = trigger_word.lower()

    def listen_for_trigger(self) -> str | None:
        """
        Listens for wake word. If detected, returns the full spoken query.
        """
        print(f"[*] Warden active. Waiting for '{self.trigger_word}'...")
        audio = ear.record_phrase(max_seconds=6, silence_limit=0.9)
        if not audio:
            return None

        text = cortex.transcribe(audio).strip()
        if not text:
            return None

        clean_text = text.lower()
        if self.trigger_word in clean_text:
            print(f"[TRIGGER DETECTED]: \"{text}\"")
            return text
        return None

wake_warden = WakeWarden()
