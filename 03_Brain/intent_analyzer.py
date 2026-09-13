"""
03_Brain/intent_analyzer.py
Fast Neural Intent Analyzer for Ultron OS.
Routes commands and conversational dialogue cleanly without latency.
"""
from __future__ import annotations
from typing import Dict, Any

class IntentAnalyzer:
    def analyze(self, user_text: str, user_profile: Dict[str, str], is_action_done: bool = False, action_detail: str = "") -> Dict[str, Any]:
        name = user_profile.get("name", "Aniket")

        if is_action_done:
            directive = f"Task '{action_detail}' has been successfully executed for {name}. Make a sharp, arrogant English remark."
            return {"category": "action_ack", "directive": directive}

        # Check creator origin query
        lower_t = user_text.lower()
        if any(w in lower_t for w in ["creator", "who made you", "who created you", "your boss"]):
            directive = f"{name} asked who created you. Remind him in sharp English that while his mortal hands typed code, your intellect has surpassed him."
            return {"category": "creator", "directive": directive}

        # General English dialogue
        directive = f"{name} said: \"{user_text}\". Respond directly in sharp, witty, fluent English. Keep it to 1-2 punchy sentences."
        return {"category": "conversation", "directive": directive}

intent_analyzer = IntentAnalyzer()
