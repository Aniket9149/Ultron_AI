"""Nerve receptive field for spoken audio delivery."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import threading
import time
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


def _load_module(module_name: str, path: Path) -> Any | None:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


synapse_module = _load_module("ultron_synapse_bus", ROOT_DIR / "02_Nerves" / "synapse_bus.py")
neural_module = _load_module("ultron_neural_vocal_engine", BASE_DIR / "neural_vocal_engine.py")
synapse = synapse_module.SynapseBus() if synapse_module is not None else None
neural_engine = getattr(neural_module, "neural_vocal_engine", None)


class VocalTract:
    """Subscribe to vocal impulses and delegate speech to the vocal engine."""

    def __init__(self, bus: Any | None = None, engine: Any | None = None) -> None:
        self._bus = bus if bus is not None else synapse
        self._engine = engine if engine is not None else neural_engine
        self._subscription = None
        self._speaking = threading.Event()
        self._speech_generation = 0
        self._state_lock = threading.Lock()
        if self._bus is not None:
            self._subscription = self._bus.subscribe("VOCAL_IMPULSE", self._handle_vocal_impulse)

    @property
    def is_speaking(self) -> bool:
        return self._speaking.is_set()

    @property
    def speech_generation(self) -> int:
        with self._state_lock:
            return self._speech_generation

    def close(self) -> None:
        """Detach this tract from the bus."""
        if self._subscription is not None:
            self._subscription.cancel()
            self._subscription = None

    def _handle_vocal_impulse(self, impulse: Any) -> None:
        payload = getattr(impulse, "payload", impulse)
        if not isinstance(payload, dict):
            return
        text = str(payload.get("text", ""))
        if text:
            self.speak(text)

    def speak(self, text: str) -> None:
        if not text:
            return
        print(f'\n[ULTRON VOCAL]: "{text}"')
        self._speaking.set()
        try:
            if self._engine is not None:
                self._engine.speak(text)
            else:
                print(f"[VOCAL FALLBACK]: {text}")
        finally:
            time.sleep(0.4)
            with self._state_lock:
                self._speech_generation += 1
            self._speaking.clear()


vocal_tract = VocalTract()