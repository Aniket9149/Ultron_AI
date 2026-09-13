"""
01_Memory/memory_cortex.py
Unified Dual-Memory System (Short-Term & Long-Term) for Ultron Studio.
"""
from __future__ import annotations
import json
import time
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import deque

MEMORY_DIR = Path(__file__).resolve().parent
LTM_FILE = MEMORY_DIR / "long_term_store.json"

class ShortTermMemory:
    """
    Sliding window buffer for immediate context, recent turns, and active goals.
    Kept volatile or bounded to prevent context bloat.
    """
    def __init__(self, capacity: int = 15):
        self.capacity = capacity
        self.buffer: deque[Dict[str, Any]] = deque(maxlen=capacity)
        self.scratchpad: Dict[str, Any] = {}

    def add(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        entry = {
            "timestamp": time.time(),
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        self.buffer.append(entry)

    def get_recent_context(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        entries = list(self.buffer)
        if limit:
            return entries[-limit:]
        return entries

    def set_scratch(self, key: str, value: Any):
        self.scratchpad[key] = value

    def get_scratch(self, key: str, default: Any = None) -> Any:
        return self.scratchpad.get(key, default)

    def clear(self):
        self.buffer.clear()
        self.scratchpad.clear()


class LongTermMemory:
    """
    Persistent key-value and episodic memory store with relevance search.
    Saves facts, architecture blueprints, rules, and user tastes.
    """
    def __init__(self, storage_path: Path = LTM_FILE):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        if not self.storage_path.exists():
            initial = {
                "version": "1.0.0",
                "last_updated": time.time(),
                "core_facts": {},          # Permanent rules, user tastes, studio configs
                "episodes": []             # Historical decisions, completed milestones
            }
            self._write(initial)

    def _read(self) -> Dict[str, Any]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"core_facts": {}, "episodes": []}

    def _write(self, data: Dict[str, Any]):
        data["last_updated"] = time.time()
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def remember_fact(self, key: str, value: Any, category: str = "general"):
        data = self._read()
        data["core_facts"][key] = {
            "value": value,
            "category": category,
            "updated_at": time.time()
        }
        self._write(data)

    def recall_fact(self, key: str, default: Any = None) -> Any:
        data = self._read()
        fact = data.get("core_facts", {}).get(key)
        return fact["value"] if fact else default

    def log_episode(self, event_type: str, summary: str, details: Optional[Dict[str, Any]] = None):
        data = self._read()
        episode = {
            "id": f"ep_{int(time.time() * 1000)}",
            "timestamp": time.time(),
            "type": event_type,
            "summary": summary,
            "details": details or {}
        }
        data["episodes"].append(episode)
        # Bounded history to prevent massive file bloat
        if len(data["episodes"]) > 300:
            data["episodes"] = data["episodes"][-300:]
        self._write(data)

    def query_episodes(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Relevance scoring using term frequency matching.
        """
        data = self._read()
        episodes = data.get("episodes", [])
        terms = set(query.lower().split())

        scored = []
        for ep in episodes:
            text = (ep["summary"] + " " + ep.get("type", "")).lower()
            score = sum(1 for term in terms if term in text)
            if score > 0:
                scored.append((score, ep))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]


class UltronMemoryCortex:
    """
    Unified coordinator combining STM & LTM.
    """
    def __init__(self):
        self.stm = ShortTermMemory(capacity=20)
        self.ltm = LongTermMemory()

    def record_turn(self, speaker: str, utterance: str, metadata: Optional[Dict[str, Any]] = None):
        self.stm.add(role=speaker, content=utterance, metadata=metadata)

    def consolidate_turn_to_ltm(self, key: str, insight: Any, category: str = "project_insight"):
        """Promotes an important short-term item into permanent memory."""
        self.ltm.remember_fact(key, insight, category=category)

    def get_prompt_context(self, current_intent: str) -> str:
        """Constructs an augmented memory context for LLM dispatchers."""
        recent_turns = self.stm.get_recent_context(limit=6)
        relevant_episodes = self.ltm.query_episodes(current_intent, limit=3)
        
        ctx_parts = []
        if relevant_episodes:
            ctx_parts.append("[LONG-TERM RELEVANT MEMORY]:")
            for ep in relevant_episodes:
                ctx_parts.append(f"- ({ep['type']}) {ep['summary']}")

        if recent_turns:
            ctx_parts.append("\n[RECENT DIALOGUE BUFFER]:")
            for t in recent_turns:
                ctx_parts.append(f"{t['role']}: {t['content']}")

        return "\n".join(ctx_parts)

memory_cortex = UltronMemoryCortex()
