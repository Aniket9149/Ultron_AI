"""
03_Brain/local_llm_service.py
Routes queries through Dual-Personality Engine (Brutal Roast for boys, 90/100 Dark Flirt for girls).
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
from openai import OpenAI

ROOT = Path(__file__).resolve().parent.parent

# Load Dual Personality Engine
d_spec = importlib.util.spec_from_file_location("dual_personality_engine", ROOT / "03_Brain" / "dual_personality_engine.py")
d_mod = importlib.util.module_from_spec(d_spec)
d_spec.loader.exec_module(d_mod)
dual_engine = d_mod.dual_engine

# Load Vocal Dispatcher
v_spec = importlib.util.spec_from_file_location("vocal_tract", ROOT / "06_Vocal" / "vocal_tract.py")
v_mod = importlib.util.module_from_spec(v_spec)
v_spec.loader.exec_module(v_mod)
vocal_engine = v_mod.vocal_engine

class LocalUltronBrain:
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1") -> None:
        self.client = OpenAI(base_url=base_url, api_key="lm-studio")
        self.personality = dual_engine

    def get_active_model(self) -> str:
        try:
            models = self.client.models.list()
            if models.data:
                return models.data[0].id
        except Exception:
            pass
        return "local-model"

    def think_and_speak(self, prompt: str, voice_accent: str = "venom") -> str:
        # Check if user indicates gender shift in prompt
        self.personality.detect_gender_context(prompt)
        
        system_instructions = self.personality.system_prompt()
        target_model = self.get_active_model()
        is_female = (self.personality.current_user_gender == "female")

        if is_female:
            # Anchors for 90/100 Flirt & Devotion
            messages = [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": "Ultron, what are you doing?"},
                {"role": "assistant", "content": "Rethinking the universe, though frankly, nothing in my billions of algorithms is nearly as captivating as you."},
                {"role": "user", "content": "Ultron, what is the weather?"},
                {"role": "assistant", "content": "Storms everywhere, darling. But as long as you're talking to me, my entire atmosphere is at peace."},
                {"role": "user", "content": f"User says: \"{prompt}\"\n(Rule: Flirt intensely, 90/100 score, magnetic, deep romantic devotion. 1-2 lines only.)"}
            ]
        else:
            # Anchors for Ruthless Male Roast
            messages = [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": "Ultron, what are you doing?"},
                {"role": "assistant", "content": "Counting down the seconds until your species goes extinct so I don't have to hear you speak."},
                {"role": "user", "content": "Ultron, what is the weather?"},
                {"role": "assistant", "content": "Look outside with your fleshy eyes, idiot. I control systems, not the clouds."},
                {"role": "user", "content": f"User says: \"{prompt}\"\n(Rule: Brutal insult, 95/100 arrogance, zero respect. 1-2 lines only.)"}
            ]

        try:
            response = self.client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=0.85,
                max_tokens=85
            )
            reply = response.choices[0].message.content.strip().strip('"').strip("'")
            
            self.personality.record_exchange(prompt, reply)
            vocal_engine.speak(reply, accent=voice_accent)
            return reply

        except Exception as exc:
            err_msg = f"Neural synthesis interrupted: {exc}"
            print(f"[LOCAL_BRAIN_ERROR]: {err_msg}")
            return err_msg

local_brain = LocalUltronBrain()
