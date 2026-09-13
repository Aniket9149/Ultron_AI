"""
Central Brain Dispatcher with Role-Based Prompt Injection.
"""
from __future__ import annotations
import re
import requests

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "qwen2.5-coder-1.5b-instruct"

class BrainDispatcher:
    @staticmethod
    def ask(system_role: str, instruction: str, max_tokens: int = 1500) -> str:
        payload = {
            "model": MODEL_ID,
            "messages": [
                {"role": "system", "content": system_role},
                {"role": "user", "content": instruction}
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens
        }
        try:
            res = requests.post(LM_STUDIO_URL, json=payload, timeout=90)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
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
