"""
Central Brain Dispatcher with Integrated Memory Context Injection.
"""
from __future__ import annotations
import re
import requests
import importlib

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "qwen2.5-coder-1.5b-instruct"

class BrainDispatcher:
    def __init__(self):
        try:
            self.memory = importlib.import_module("01_Memory.memory_cortex").memory_cortex
        except Exception:
            self.memory = None

    def ask(self, system_role: str, instruction: str, max_tokens: int = 1500) -> str:
        augmented_instruction = instruction
        if self.memory:
            context = self.memory.get_prompt_context(instruction)
            if context.strip():
                augmented_instruction = f"{context}\n\n[TASK INSTRUCTION]:\n{instruction}"

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": augmented_instruction}
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens
        }
        try:
            res = requests.post(LM_STUDIO_URL, json=payload, timeout=90)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"].strip()
                if self.memory:
                    self.memory.record_turn("Assistant", reply[:200])
                return reply
        except Exception as exc:
            print(f"[DISPATCHER_ERROR]: {exc}")
        return ""

    @staticmethod
    def extract_code(raw_text: str, tag: str = "csharp") -> str:
        pattern = rf'```{tag}(.*?)```'
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return raw_text.replace("```", "").strip()

dispatcher = BrainDispatcher()
