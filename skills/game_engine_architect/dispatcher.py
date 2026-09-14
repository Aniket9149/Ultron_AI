"""
Central Brain Dispatcher with Live Connectivity Guard.
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

    def check_connection(self) -> bool:
        try:
            r = requests.get("http://127.0.0.1:1234/v1/models", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def ask(self, system_role: str, instruction: str, max_tokens: int = 1500) -> str:
        augmented = instruction
        if self.memory:
            ctx = self.memory.get_prompt_context(instruction)
            if ctx.strip():
                augmented = f"{ctx}\n\n[TASK INSTRUCTION]:\n{instruction}"

        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": augmented}
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
            print(f"\n[DISPATCHER_OFFLINE]: LM Studio port 1234 unreachable. Pehle LM Studio mein Start Server click karo.")
        return ""

    @staticmethod
    def extract_code(raw_text: str, tag: str = "csharp") -> str:
        pattern = rf'```{tag}(.*?)```'
        match = re.search(pattern, raw_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return raw_text.replace("```", "").strip()

dispatcher = BrainDispatcher()
