"""
06_Vocal/acoustic_damper.py
Prevents mic feedback while Ultron voice engine is synthesizing speech.
"""
import threading

class AcousticDamper:
    def __init__(self) -> None:
        self._is_speaking = threading.Event()

    def engage(self) -> None:
        self._is_speaking.set()

    def disengage(self) -> None:
        self._is_speaking.clear()

    @property
    def is_active(self) -> bool:
        return self._is_speaking.is_set()

damper = AcousticDamper()
