"""
main_loop.py
Gender-Adaptive Ultron Runtime with Voice Trigger & 90s Attention.
"""
import importlib.util
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

print("\n" + "="*60)
print("[*] BOOTING ULTRON DUAL-CORE OS...")
print("="*60)

# Load Modules
d_spec = importlib.util.spec_from_file_location("dual_personality_engine", ROOT / "03_Brain" / "dual_personality_engine.py")
d_mod = importlib.util.module_from_spec(d_spec)
d_spec.loader.exec_module(d_mod)
personality = d_mod.dual_engine

v_spec = importlib.util.spec_from_file_location("vocal_tract", ROOT / "06_Vocal" / "vocal_tract.py")
v_mod = importlib.util.module_from_spec(v_spec)
v_spec.loader.exec_module(v_mod)
vocal_engine = v_mod.vocal_engine

b_spec = importlib.util.spec_from_file_location("local_llm_service", ROOT / "03_Brain" / "local_llm_service.py")
b_mod = importlib.util.module_from_spec(b_spec)
b_spec.loader.exec_module(b_mod)
brain = b_mod.local_brain

e_spec = importlib.util.spec_from_file_location("ear_stream", ROOT / "04_Senses" / "ear_stream.py")
e_mod = importlib.util.module_from_spec(e_spec)
e_spec.loader.exec_module(e_mod)
ear = e_mod.ear_stream

s_spec = importlib.util.spec_from_file_location("speech_cortex", ROOT / "04_Senses" / "speech_cortex.py")
s_mod = importlib.util.module_from_spec(s_spec)
s_spec.loader.exec_module(s_mod)
cortex = s_mod.speech_cortex

# Startup Voice
startup_greeting = personality.get_boot_greeting()
print(f"\n[ULTRON BOOT]: {startup_greeting}\n")
vocal_engine.speak(startup_greeting, accent="venom")

SESSION_TIMEOUT = 90.0
active_session_until = time.time() + SESSION_TIMEOUT

print("="*60)
print(f"[*] ULTRON ACTIVE - Attention Window: 90s")
print("Say 'I am a girl' to switch to Flirt Mode, or 'I am a boy' for Roast Mode.")
print("="*60 + "\n")

try:
    while True:
        now = time.time()
        in_active_window = (now < active_session_until)

        audio = ear.record_phrase(max_seconds=7, silence_limit=0.9)
        if not audio:
            continue

        spoken_text = cortex.transcribe(audio).strip()
        if not spoken_text:
            continue

        clean_lower = spoken_text.lower()

        if "ultron" in clean_lower or in_active_window:
            active_session_until = time.time() + SESSION_TIMEOUT
            print(f"\n[User]: \"{spoken_text}\"")
            reply = brain.think_and_speak(spoken_text, voice_accent="venom")
            print(f"[Ultron]: {reply}\n")

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n[*] Ultron shutting down.")
