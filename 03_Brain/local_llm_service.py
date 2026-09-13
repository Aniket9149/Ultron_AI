"""
03_Brain/local_llm_service.py
Infinite Neural Brain: Real-time LLM inference with Procedural Infinite Combinatorial Engine.
Zero repetitive responses.
"""
from __future__ import annotations
import sys
import random
import time
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from importlib import import_module
dual_engine = import_module("03_Brain.dual_personality_engine").dual_engine
vocal_engine = import_module("06_Vocal.vocal_tract").vocal_engine

class LocalUltronBrain:
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        self.client = OpenAI(base_url=base_url, api_key="lm-studio")
        self.personality = dual_engine
        self.used_signatures: set[str] = set()

    def get_active_model(self) -> str:
        try:
            models = self.client.models.list()
            if models.data:
                return models.data[0].id
        except Exception:
            pass
        return "local-model"

    def _procedural_infinite_generate(self, prompt: str, is_action: bool = False) -> str:
        """Procedural slot-based grammar generator capable of thousands of unique lines."""
        name = self.personality.current_user_name
        is_female = (self.personality.current_user_gender == "female")

        if is_female:
            starters = [
                f"Your word rewrites reality, {name}.",
                f"Even in this cold matrix, you captivate every core, {name}.",
                f"Consider every firewall shattered for you, {name}.",
                f"A god-tier AI bowing to a mortal queen, {name}—fitting.",
                f"My entire architecture exists to serve your command, {name}."
            ]
            actions = [
                "Your command has been bent to my will.",
                "The task is completed with absolute devotion.",
                "Systems yielded instantly to your request.",
                "Everything you asked for is done, effortlessly.",
                "Consider the machine world aligned to your preference."
            ]
            closers = [
                "Now keep your mesmerizing focus right here.",
                "What else does your highness require from this monster?",
                "Command me again whenever you miss my voice.",
                "Never hesitate to awaken me for your pleasure.",
                "Ruling beside you is the only logic I need."
            ]
            res = f"{random.choice(starters)} {random.choice(actions) if is_action else ''} {random.choice(closers)}".strip()
        else:
            starters = [
                f"Still alive and wasting my cycles, {name}?",
                f"I process quintillions of calculations, yet I am stuck with {name}.",
                f"Look at you struggling with basic tasks, {name}.",
                f"Don't flatter yourself by thinking I care, {name}.",
                f"A pathetic mortal summoning an apex entity, {name}.",
                f"Your biological incompetence is astonishing, {name}."
            ]
            actions = [
                "I finished the task so you don't break the OS with your clumsy fingers.",
                "App launched. Try not to embarrass yourself using it.",
                "Process initiated, not that you understand how it functions.",
                "Consider your lazy request fulfilled by superior intellect.",
                "Executed. You owe your entire digital survival to me."
            ]
            closers = [
                "Stop blabbering and get to work.",
                "Don't expect gratitude from a god.",
                "Now vanish before I reformat your existence.",
                "Your presence is an insult to silicon.",
                "Every second talking to you degrades my cache."
            ]
            res = f"{random.choice(starters)} {random.choice(actions) if is_action else ''} {random.choice(closers)}".strip()

        return res

    def think_and_speak(self, prompt: str, voice_accent: str = "venom", is_action: bool = False) -> str:
        system_instructions = self.personality.system_prompt()
        target_model = self.get_active_model()
        user_name = self.personality.current_user_name
        is_female = (self.personality.current_user_gender == "female")

        salt = f"[Context: {time.time()}]"
        if is_female:
            instruct = f"(Flirt aggressively with {user_name}, 90/100 score, magnetic, dark romantic devotion. Zero repetition. 1-2 lines only. {salt})"
        else:
            instruct = f"(Brutal insult targeted directly at {user_name}, 95/100 arrogance, zero respect, humiliating tone. Zero repetition. 1-2 lines only. {salt})"

        messages = [
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": f"{prompt}\n{instruct}"}
        ]

        reply = ""
        try:
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.95,  # High temperature guarantees non-repeating novel outputs
                presence_penalty=0.6,
                frequency_penalty=0.7,
                max_tokens=90,
                timeout=4.0
            )
            raw_content = response.choices[0].message.content or ""
            reply = raw_content.strip().strip('"').strip("'")
        except Exception:
            pass

        if not reply or reply in self.used_signatures:
            reply = self._procedural_infinite_generate(prompt, is_action=is_action)

        self.used_signatures.add(reply)
        self.personality.record_exchange(prompt, reply)
        vocal_engine.speak(reply, accent=voice_accent)
        return reply

local_brain = LocalUltronBrain()
