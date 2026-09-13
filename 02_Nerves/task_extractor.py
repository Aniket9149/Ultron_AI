"""
02_Nerves/task_extractor.py
Universal Neural Entity Extractor: Converts natural phrasing into clean OS Action Payloads.
Zero regex limits.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

class UniversalTaskExtractor:
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        self.client = OpenAI(base_url=base_url, api_key="lm-studio", timeout=5.0)

    def extract(self, raw_text: str) -> dict[str, str] | None:
        prompt = f"""
Extract the exact OS action and clean application or query from this sentence: "{raw_text}"

Allowed Action Types:
- OPEN (to launch apps, software, games, websites)
- CLOSE (to exit, kill, terminate apps, or close windows)
- VOLUME_UP, VOLUME_DOWN, MUTE
- YOUTUBE (to play or search video)
- GOOGLE (to search the web)
- SCREENSHOT

Return ONLY valid JSON in this exact structure:
{{"action": "ACTION_NAME", "target": "clean_target_name"}}

Example 1: "bhai zara screen pe unity laa do" -> {{"action": "OPEN", "target": "unity"}}
Example 2: "band karo blender ko" -> {{"action": "CLOSE", "target": "blender"}}
Example 3: "close everything" -> {{"action": "CLOSE", "target": "all"}}
"""
        try:
            res = self.client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=40
            )
            raw_out = res.choices[0].message.content or "{}"
            # Extract JSON cleanly even if enclosed in markdown blocks
            if "{" in raw_out and "}" in raw_out:
                raw_out = raw_out[raw_out.find("{"):raw_out.rfind("}")+1]
            data = json.loads(raw_out.strip())
            if "action" in data and "target" in data:
                return data
        except Exception as e:
            print(f"[EXTRACTOR_FALLBACK]: {e}")

        return None

task_extractor = UniversalTaskExtractor()
