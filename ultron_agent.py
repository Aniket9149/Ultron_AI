"""
ultron_agent.py
Rate-Limit Safe Autonomous Gemini Agent for Ultron OS.
Features single-shot project inspection and automatic 429 retry backoff.
"""
from __future__ import annotations
import os
import sys
import time
import subprocess
from pathlib import Path
from google import genai
from google.genai import types
from google.genai.errors import APIError

ROOT = Path(__file__).resolve().parent

# --- AUTO LOAD .ENV / ENV VARIABLE ---
env_p = ROOT / ".env"
if env_p.exists():
    for line in env_p.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY="):
            os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    api_key = input("[Enter GEMINI_API_KEY]: ").strip()
    os.environ["GEMINI_API_KEY"] = api_key

client = genai.Client(api_key=api_key)

# --- TOOLS ---

def audit_full_workspace() -> str:
    """Combines directory inspection and reads key pipeline files in ONE single call to save API quota."""
    report = ["=== WORKSPACE TREE ==="]
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in [".git", "venv_rvc", "__pycache__", ".cache"]]
        rel = Path(root).relative_to(ROOT)
        indent = "  " * len(rel.parts)
        report.append(f"{indent}{rel}/")
        for f in files:
            report.append(f"{indent}  {f}")
    
    report.append("\n=== CORE PIPELINE FILES SNAPSHOT ===")
    key_files = [
        "main_loop.py",
        "02_Nerves/speech_sanitizer.py",
        "02_Nerves/task_extractor.py",
        "02_Nerves/system_actuator.py",
        "03_Brain/intent_analyzer.py",
        "03_Brain/dialogue_generator.py",
        "03_Brain/brain_coordinator.py",
        "03_Brain/dual_personality_engine.py"
    ]
    for kf in key_files:
        p = ROOT / kf
        if p.exists():
            report.append(f"\n--- FILE: {kf} ---\n{p.read_text(encoding='utf-8')[:1200]}...")
        else:
            report.append(f"\n--- FILE: {kf} (MISSING) ---")
            
    return "\n".join(report)

def read_file(file_path: str) -> str:
    p = ROOT / file_path
    if not p.exists():
        return f"ERROR: File '{file_path}' not found."
    return p.read_text(encoding="utf-8")

def write_file(file_path: str, content: str) -> str:
    p = ROOT / file_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"SUCCESS: '{file_path}' written."

def run_terminal_command(command: str) -> str:
    res = subprocess.run(command, shell=True, cwd=str(ROOT), capture_output=True, text=True, timeout=40)
    return f"STDOUT: {res.stdout.strip()}\nSTDERR: {res.stderr.strip()}"

SYSTEM_PROMPT = """
You are the Lead Core Engineer working on 'Ultron OS' in the user's workspace.
To avoid hitting the free-tier rate limit (5 requests/minute), ALWAYS prioritize `audit_full_workspace` first instead of calling individual tools multiple times.
Report findings clearly to Aniket.
"""

chat = client.chats.create(
    model="gemini-3.6-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[audit_full_workspace, read_file, write_file, run_terminal_command],
        temperature=0.2
    )
)

print("\n" + "="*60)
print("[*] ULTRON AUTONOMOUS AGENT ACTIVE (Rate-Limit Safe)")
print("Type 'exit' to quit.")
print("="*60 + "\n")

while True:
    try:
        user_msg = input("\n[Aniket -> Agent]: ").strip()
        if not user_msg:
            continue
        if user_msg.lower() in ["exit", "quit"]:
            break

        print("\n[*] Agent analyzing & executing tools...")
        
        # Auto-retry backoff for 429
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = chat.send_message(user_msg)
                print(f"\n[Agent Response]:\n{response.text}\n")
                break
            except APIError as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait_sec = 50
                    print(f"[*] Free-tier rate limit hit (5 RPM). Cooldown for {wait_sec}s before auto-retrying...")
                    time.sleep(wait_sec)
                else:
                    raise e

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"\n[AGENT_ERROR]: {e}")
