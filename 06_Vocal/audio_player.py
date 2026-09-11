"""
06_Vocal/audio_player.py
High-level player coordinating damper and speech output.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent

def _load(name: str, file: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_damper_mod = _load("acoustic_damper", "acoustic_damper.py")
_tract_mod = _load("vocal_tract", "vocal_tract.py")

damper = _damper_mod.damper
vocal_engine = _tract_mod.vocal_engine

class AudioPlayer:
    @staticmethod
    def output_speech(payload: Dict[str, Any]) -> None:
        text = payload.get("text", "")
        if not text:
            return
        try:
            damper.engage()
            print(f"\n[ULTRON VOCAL]: \"{text}\"")
            vocal_engine.speak(text)
        finally:
            damper.disengage()

player = AudioPlayer()
