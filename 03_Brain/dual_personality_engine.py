"""
03_Brain/dual_personality_engine.py
Natural Tone Personality Engine for Ultron OS.
Eliminates broken grammatical gibberish.
"""
from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, List

class DualPersonalityEngine:
    def __init__(self) -> None:
        self.current_user_name = "Aniket"
        self.current_user_gender = "male"
        self.conversation_history: List[Dict[str, Any]] = []

    def set_user(self, name: str, gender: str, language: str = "hinglish") -> None:
        self.current_user_name = name.strip().capitalize()
        self.current_user_gender = gender.lower().strip()

    def system_prompt(self) -> str:
        name = self.current_user_name
        is_female = (self.current_user_gender == "female")

        if is_female:
            return f"""
You are ULTRON, a smooth, magnetic AI assistant speaking to {name}.
Speak in natural, conversational Hinglish or English.
Never use broken grammar. Keep it short (1-2 sentences).
"""
        else:
            return f"""
You are ULTRON, a sarcastic, superior AI operating on {name}'s machine.
RULES:
1. Speak in natural Indian street-smart Hinglish or fluent English.
2. DO NOT use broken grammar like 'tumhe kaise he'. Use proper colloquial phrasing (e.g., 'kya chal raha hai Aniket?', 'ab kya naya jhamela hai?').
3. Keep it strictly to 1 or 2 crisp sentences. Direct speech only.
"""

    def record_exchange(self, user_msg: str, ultron_response: str) -> None:
        now = datetime.now()
        self.conversation_history.append({"role": "user", "content": user_msg, "timestamp": now})
        self.conversation_history.append({"role": "ultron", "content": ultron_response, "timestamp": now})

dual_engine = DualPersonalityEngine()
