"""
03_Brain/brain_coordinator.py
Coordinates Intent Evaluation, Personality Constraints, and Dialogue Generation.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from importlib import import_module
dual_engine = import_module("03_Brain.dual_personality_engine").dual_engine
intent_analyzer = import_module("03_Brain.intent_analyzer").intent_analyzer
dialogue_generator = import_module("03_Brain.dialogue_generator").dialogue_generator
vocal_engine = import_module("06_Vocal.vocal_tract").vocal_engine

class BrainCoordinator:
    def __init__(self) -> None:
        self.personality = dual_engine
        self.analyzer = intent_analyzer
        self.generator = dialogue_generator

    def process(self, user_text: str, is_action_done: bool = False, action_detail: str = "", voice_accent: str = "venom") -> str:
        profile = {
            "name": self.personality.current_user_name,
            "gender": self.personality.current_user_gender
        }

        # 1. Decide what kind of response to produce
        analysis = self.analyzer.analyze(
            user_text=user_text,
            user_profile=profile,
            is_action_done=is_action_done,
            action_detail=action_detail
        )

        # 2. Get current system personality instructions
        sys_prompt = self.personality.system_prompt()

        # 3. Generate pure dynamic dialogue via local model
        reply = self.generator.generate(
            directive=analysis["directive"],
            system_prompt=sys_prompt,
            user_name=profile["name"]
        )

        # 4. Save history & Speak
        self.personality.record_exchange(user_text, reply)
        vocal_engine.speak(reply, accent=voice_accent)
        return reply

brain_coordinator = BrainCoordinator()
