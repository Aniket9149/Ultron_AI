"""
03_Brain/dialogue_generator.py
Dedicated neural generator with Strict Output Sanitizer and Tag Stripper.
"""
from __future__ import annotations
import sys
import time
import re
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

class DialogueGenerator:
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        self.client = OpenAI(base_url=base_url, api_key="lm-studio", timeout=15.0)
        self.model_name = "local-model"
        self._refresh_model()

    def _refresh_model(self) -> None:
        try:
            models = self.client.models.list()
            if models.data:
                self.model_name = models.data[0].id
        except Exception:
            pass

    def _sanitize(self, raw_text: str, user_name: str) -> str:
        text = raw_text.strip()
        # Remove markdown tags like [Entropy: ...] or [Irrelevance: ...]
        text = re.sub(r"\[.*?\]", "", text)
        # Remove prompt echo like "Aniket said: ..."
        text = re.sub(rf"^{user_name}\s+said:?.*?\n", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^assistant:?", "", text, flags=re.IGNORECASE)
        # Strip excessive outer quotes
        text = text.strip('"\' \n')
        # Limit to 2 sentences max to prevent rambling
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        if len(sentences) > 2:
            text = " ".join(sentences[:2])
        return text.strip()

    def generate(self, directive: str, system_prompt: str, user_name: str) -> str:
        self._refresh_model()
        salt = f"t_{time.time_ns() % 100000}"

        messages = [
            {"role": "system", "content": f"{system_prompt}\nCRITICAL: Respond ONLY with the spoken dialogue. Do NOT repeat what the user said. Do NOT add meta tags or explanations. Maximum 2 sentences."},
            {"role": "user", "content": f"Instruction: {directive}\nSeed: {salt}\nDialogue:"}
        ]

        try:
            start_t = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.88,
                presence_penalty=0.5,
                frequency_penalty=0.5,
                max_tokens=65,
                stop=["\n[", "User said:", f"{user_name} said:"]
            )
            elapsed = round(time.time() - start_t, 2)
            content = response.choices[0].message.content or ""
            clean_reply = self._sanitize(content, user_name)

            if not clean_reply:
                clean_reply = f"Stop babbling, {user_name}, and give me a coherent command."

            print(f"[GENERATOR]: Response generated in {elapsed}s.")
            return clean_reply

        except Exception as err:
            print(f"[GENERATOR ERROR]: {err}")
            return f"My neural link is recalibrating, {user_name}. Speak again."

dialogue_generator = DialogueGenerator()
