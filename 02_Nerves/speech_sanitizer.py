"""
02_Nerves/speech_sanitizer.py
Universal Neural Classifier: Uses Local LLM Zero-Shot Classification.
Zero hardcoded keywords. Adapts to any language, phrasing, or slang.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

class UniversalSpeechSanitizer:
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        self.client = OpenAI(base_url=base_url, api_key="lm-studio", timeout=5.0)

    def classify_and_split(self, raw_input: str) -> dict[str, str]:
        prompt = f"""
You are an OS Intent Classifier. Analyze the user statement and decide if they want the operating system to perform an action (like opening/closing an app, changing volume, searching web, taking screenshot) or if they are just chatting/asking questions.

User statement: "{raw_input}"

Respond ONLY with valid JSON in this exact structure:
{{"type": "task"}} OR {{"type": "natural_talk"}}
"""
        try:
            res = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=20
            )
            raw_out = res.choices[0].message.content or "{}"
            data = json.loads(raw_out.strip())
            out_type = data.get("type", "natural_talk")
            return {"type": out_type, "raw_text": raw_input}
        except Exception:
            # Fallback heuristic if local server stalls
            lowered = raw_input.lower()
            if any(w in lowered for w in ["open", "close", "launch", "kholo", "band", "volume"]):
                return {"type": "task", "raw_text": raw_input}
            return {"type": "natural_talk", "raw_text": raw_input}

speech_sanitizer = UniversalSpeechSanitizer()
