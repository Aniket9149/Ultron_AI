import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Load Ear Stream
e_spec = importlib.util.spec_from_file_location("ear_stream", ROOT / "04_Senses" / "ear_stream.py")
e_mod = importlib.util.module_from_spec(e_spec)
e_spec.loader.exec_module(e_mod)
ear = e_mod.ear_stream

# Load Speech Cortex
s_spec = importlib.util.spec_from_file_location("speech_cortex", ROOT / "04_Senses" / "speech_cortex.py")
s_mod = importlib.util.module_from_spec(s_spec)
s_spec.loader.exec_module(s_mod)
cortex = s_mod.speech_cortex

print("\n" + "="*50)
print("[*] TEST: SENSORY AUDIO PIPELINE")
print("Press Enter to speak...")
input()

audio_data = ear.record_phrase(max_seconds=6)
if audio_data:
    recognized_text = cortex.transcribe(audio_data)
    print(f"\n[Transcribed Text]: \"{recognized_text}\"")
else:
    print("[*] No voice input recorded.")
print("="*50)
