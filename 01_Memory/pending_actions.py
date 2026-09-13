"""
01_Memory/pending_actions.py
File-backed persistent state store for confirmation dialogs.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

STATE_FILE = Path(__file__).resolve().parent / "pending_state.json"

class PendingActionStore:
    def set_pending(self, action_type: str, path: str, context: dict[str, Any] = None) -> None:
        data = {
            "type": action_type,
            "path": path,
            "context": context or {}
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def get_pending(self) -> dict[str, Any] | None:
        if not STATE_FILE.exists():
            return None
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def clear(self) -> None:
        if STATE_FILE.exists():
            try:
                STATE_FILE.unlink()
            except Exception:
                pass

pending_store = PendingActionStore()
