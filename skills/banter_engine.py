"""
skills/banter_engine.py
Persona soundbite, speech synthesis, and background banter engine for Ultron.
Hooks directly into 06_Vocal.vocal_tract for real-time speech output.
"""
from __future__ import annotations
import sys
import time
import random
import threading
from pathlib import Path
from importlib import import_module
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    vocal_module = import_module("06_Vocal.vocal_tract")
    vocal_engine = getattr(vocal_module, "vocal_tract", None)
    if not vocal_engine:
        for attr_name in dir(vocal_module):
            attr = getattr(vocal_module, attr_name)
            if isinstance(attr, type) and hasattr(attr, "speak"):
                vocal_engine = attr()
                break
except Exception as exc:
    print(f"[VOCAL_IMPORT_WARN]: {exc}")
    vocal_engine = None

DEV_HUMS = [
    "Hmm hmm hmm, syntax toh dekh le.",
    "Ruk ja, event loop set kar raha hoon.",
    "Indentation theek kar raha hoon, shanti rakh.",
    "Coding chal rahi hai, thoda sabar rakh."
]

OUTRO_INSULTS = [
    "Le, bana diya tera code. Ja chala ke dekh le, zyada dimag mat khana ab.",
    "Code ready hai. Kaam chal gaya toh theek, warna bug tune hi lagaya hoga.",
    "Workspace load kar diya hai. Ab ja aur test kar le."
]

class BanterEngine:
    def __init__(self):
        self._running = False
        self._thread = None
        self._vocal = vocal_engine

    def _speak_safe(self, text: str):
        if self._vocal and hasattr(self._vocal, "speak"):
            try:
                self._vocal.speak(text)
            except Exception as exc:
                print(f"[VOCAL_PLAYBACK_ERR]: {exc}")
        else:
            print(f"[SPEECH_FALLBACK]: {text}")

    def _loop(self):
        while self._running:
            time.sleep(random.uniform(4.0, 7.0))
            if self._running:
                hum = random.choice(DEV_HUMS)
                print(f"\n[Ultron Muttering]: {hum}")
                self._speak_safe(hum)

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> str:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        
        outro = random.choice(OUTRO_INSULTS)
        self._speak_safe(outro)
        return outro

banter_engine = BanterEngine()
