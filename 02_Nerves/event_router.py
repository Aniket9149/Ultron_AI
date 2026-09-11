"""
02_Nerves/event_router.py
Layer 2: Priority classification and handler registration core.
"""
from __future__ import annotations
from collections import defaultdict
import threading
from typing import Any, Callable, Dict, List

EMERGENCY_TOPICS = {"SHUTDOWN", "SYSTEM_CRASH", "KILL_SWITCH", "AUDIO_PANIC"}
LOW_PRIORITY_TOPICS = {"HEARTBEAT", "RAM_TELEMETRY", "CPU_TELEMETRY", "IDLE_PULSE"}


class EventRouter:
    def __init__(self) -> None:
        self._registry: Dict[str, List[Callable[[Dict[str, Any]], Any]]] = defaultdict(list)
        self._lock = threading.Lock()

    def register(self, topic: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        with self._lock:
            if handler not in self._registry[topic]:
                self._registry[topic].append(handler)

    def resolve_handlers(self, topic: str) -> List[Callable[[Dict[str, Any]], Any]]:
        with self._lock:
            return list(self._registry.get(topic, []))

    @staticmethod
    def classify_priority(topic: str) -> int:
        """Lower numerical value equates to higher priority."""
        if topic in EMERGENCY_TOPICS:
            return 0
        if topic in LOW_PRIORITY_TOPICS:
            return 2
        return 1
