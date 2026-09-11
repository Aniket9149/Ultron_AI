"""
02_Nerves/telemetry_filter.py
Layer 1: Filters raw incoming signal packets and sanitizes telemetry.
"""
from __future__ import annotations
from typing import Any, Dict, Optional


class TelemetryFilter:
    @staticmethod
    def sanitize(topic: str, payload: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Validate topic and clean payload packet before routing."""
        if not isinstance(topic, str) or not topic.strip():
            return None

        if payload is None:
            clean_payload: Dict[str, Any] = {}
        elif isinstance(payload, dict):
            clean_payload = dict(payload)
        else:
            return None

        clean_payload.setdefault("timestamp", None)
        return clean_payload
