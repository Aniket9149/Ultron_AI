"""
06_Vocal/vocal_tract.py
Unified Vocal Controller:
- US: J.A.R.V.I.S. / David
- IN: Natural Indian English (Prabhat Neural)
- VENOM: Monstrous Symbiote Beast Layer
"""
from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def _load(mod_name: str, file_name: str):
    spec = importlib.util.spec_from_file_location(mod_name, ROOT / file_name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_us_mod = _load("voice_us", "voice_us.py")
_in_mod = _load("voice_in", "voice_in.py")
_venom_mod = _load("voice_venom", "voice_venom.py")

class VocalTractDispatcher:
    def __init__(self) -> None:
        self.us = _us_mod.voice_us
        self.indian = _in_mod.voice_in
        self.venom = _venom_mod.voice_venom

    def speak(self, text: str, accent: str = "us") -> None:
        acc = accent.lower()
        if acc in ("venom", "monster", "dark", "demon"):
            self.venom.speak(text)
        elif acc in ("in", "indian", "hi", "hinglish"):
            self.indian.speak(text)
        else:
            self.us.speak(text)

vocal_engine = VocalTractDispatcher()
