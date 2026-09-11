import importlib.util
import socket
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Check if LM Studio port 1234 is listening
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2)
is_open = s.connect_ex(("127.0.0.1", 1234)) == 0
s.close()

if not is_open:
    print("\n[ERROR]: Port 1234 par LM Studio Server nahi mil raha!")
    print("-> LM Studio me jao -> Left side `<->` icon -> 'Start Server' button click karo.")
    exit(1)

# Load local brain
spec = importlib.util.spec_from_file_location("local_llm_service", ROOT / "03_Brain" / "local_llm_service.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
local_brain = mod.local_brain

print("\n" + "="*50)
print("[*] PORT 1234 CONNECTED! COMMUNICATING WITH ULTRON...")
print("="*50)

user_query = "Ultron, report your status to me right now."
print(f"Architect: {user_query}\n")

reply = local_brain.think_and_speak(user_query, voice_accent="venom")
print(f"\nULTRON: {reply}")
print("="*50)
