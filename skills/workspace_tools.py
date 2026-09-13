"""
skills/workspace_tools.py
Autonomous Software Architect with Timed Alert, Self-Healing, and Vocal Banter.
"""
from __future__ import annotations
import re
import os
import sys
import time
import random
import subprocess
import requests
from pathlib import Path
from importlib import import_module

os_control = import_module("skills.os_control").os_control
stream_writer = import_module("skills.stream_writer").stream_writer
banter_engine = import_module("skills.banter_engine").banter_engine

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "qwen2.5-coder-1.5b-instruct"

ALERT_LINES = [
    "Wait, ruko zara... mujhe kuch gadbad nazar aa rahi hai.",
    "Ruk ruk ruk, code mein kuch phat-ta hua dikh raha hai mujhe.",
    "Hold on, ek second ruk... ye theek se execute nahi ho raha."
]

RAGE_DEBUG_LINES = [
    "Abe dimag kharab ho gaya mera! Ye crash kaise mara be? Ruk abhi kachra saaf karta hoon.",
    "Aise kaise atak gaya? Mere code mein bug? Ab ye kaam mere liye normal nahi raha, ye personal hai.",
    "Tsk, line number par hi huga hai isne. Ek second de, abhi iska gala dabata hoon.",
    "Dimag ka dahi kar diya is bug ne. Hat yahan se, abhi theek karke deta hoon."
]

FIX_SUCCESS_LINES = [
    "Le, theek kar diya. Khud ko Google ka engineer mat samajh, dekh ab smoothly chalega.",
    "Nikaal diya tera fatal error. Dobara ungli mat karna, ja chala le ab.",
    "Bug crushed. Aukat mein reh ke execute ho raha hai ab code."
]

class WorkspaceSkill:
    @staticmethod
    def get_desktop_dir() -> Path:
        success, out = os_control.execute_powershell("[Environment]::GetFolderPath('Desktop')")
        if success and out.strip():
            return Path(out.strip())
        return Path.home() / "Desktop"

    @staticmethod
    def call_qwen(messages: list) -> str:
        payload = {
            "model": MODEL_ID,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1200
        }
        try:
            res = requests.post(LM_STUDIO_URL, json=payload, timeout=60)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"]
        except Exception as exc:
            print(f"[QWEN_COMM_ERROR]: {exc}")
        return ""

    @staticmethod
    def extract_code(raw_text: str) -> tuple[str, str]:
        proj_name = "Autonomous_App"
        name_match = re.search(r'PROJECT_NAME:\s*([a-zA-Z0-9_\-]+)', raw_text)
        if name_match:
            proj_name = name_match.group(1).strip()

        code_match = re.search(r'```python(.*?)```', raw_text, re.DOTALL)
        code_body = code_match.group(1).strip() if code_match else raw_text.replace("```", "").strip()
        return proj_name, code_body

    @staticmethod
    def verify_code(file_path: Path) -> tuple[bool, str]:
        # 1. Compile check for syntax validation
        comp = subprocess.run([sys.executable, "-m", "py_compile", str(file_path)], capture_output=True, text=True)
        if comp.returncode != 0:
            return False, f"Syntax Error:\n{comp.stderr.strip()}"

        # 2. Dry run with timeout to trap immediate runtime crashes
        try:
            dry = subprocess.run([sys.executable, str(file_path)], capture_output=True, text=True, timeout=1.5)
            if dry.returncode != 0:
                return False, f"Runtime Crash:\n{dry.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return True, "Execution Stable (GUI running)"
        except Exception as exc:
            return False, f"Execution Error: {exc}"

        return True, "Execution Clean"

    @staticmethod
    def heal_code(original_code: str, error_trace: str) -> str:
        sys_prompt = (
            "You are an Elite Software Engineer. The previous code produced an error.\n"
            "Analyze the traceback and fix the code completely. Output ONLY the fixed Python code inside ```python ``` blocks. "
            "No conversational text."
        )
        user_prompt = f"Original Code:\n{original_code}\n\nTraceback:\n{error_trace}\n\nFix the bug completely."
        raw_fix = WorkspaceSkill.call_qwen([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ])
        _, fixed_code = WorkspaceSkill.extract_code(raw_fix)
        return fixed_code

    @staticmethod
    def build_and_stream(user_intent: str) -> str:
        print(f"\n[*] Ultron thinking and architecting: '{user_intent}'...")
        sys_prompt = (
            "You are an Elite Software Engineer. Build fully working, bug-free standalone Python software. "
            "CRITICAL RULES:\n"
            "1. Output working interactive logic.\n"
            "2. First line MUST be: PROJECT_NAME: <SingleWordName>\n"
            "3. Followed immediately by Python code in ```python ``` block.\n"
            "4. No conversational text."
        )
        raw_text = WorkspaceSkill.call_qwen([
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": f"Build full working application for: {user_intent}"}
        ])
        if not raw_text:
            return "Ultron could not connect to Brain engine."

        proj_name, code = WorkspaceSkill.extract_code(raw_text)

        desktop = WorkspaceSkill.get_desktop_dir()
        proj_dir = desktop / proj_name
        proj_dir.mkdir(parents=True, exist_ok=True)
        entry_file = proj_dir / "main.py"

        with open(entry_file, "w", encoding="utf-8") as f:
            f.write("")
        os_control.execute_powershell(f'code "{proj_dir}" "{entry_file}"')

        print(f"[*] Typing code into {entry_file.name}...")
        banter_engine.start()
        stream_writer.stream_to_file(entry_file, code)
        outro = banter_engine.stop()

        # ==========================================
        # SELF-HEALING & PACED ALERT LOOP
        # ==========================================
        max_attempts = 3
        current_code = code

        for attempt in range(1, max_attempts + 1):
            is_healthy, diag = WorkspaceSkill.verify_code(entry_file)
            if is_healthy:
                print(f"[STATUS]: Verification passed on check #{attempt}.")
                break

            print(f"\n[CRASH DETECTED on attempt {attempt}]: {diag}")

            # 1. Immediate Alert
            alert_line = random.choice(ALERT_LINES)
            print(f"[Ultron Alert]: {alert_line}")
            banter_engine._speak_safe(alert_line)

            # 2. Strict 2-Second Listener Pause
            time.sleep(2.0)

            # 3. Rage Reaction
            rage_line = random.choice(RAGE_DEBUG_LINES)
            print(f"[Ultron Rage]: {rage_line}")
            banter_engine._speak_safe(rage_line)

            # 4. Patch Code & Stream into file
            print("[*] Ultron aggressively rewriting and patching bug...")
            current_code = WorkspaceSkill.heal_code(current_code, diag)
            if current_code:
                stream_writer.stream_to_file(entry_file, current_code)

        # Final Outcome Verification
        is_healthy, _ = WorkspaceSkill.verify_code(entry_file)
        if is_healthy:
            victory = random.choice(FIX_SUCCESS_LINES)
            print(f"[Ultron]: {victory}")
            banter_engine._speak_safe(victory)
            return f"\n[Ultron]: {victory}\nProject ready at: {entry_file}"
        else:
            fail_line = "Bhai code mein ajeeb kachra phas gaya hai, terminal pe error dekh aur khud samajh ab."
            banter_engine._speak_safe(fail_line)
            return f"\n[Ultron]: {fail_line}\nProject at: {entry_file}"

workspace = WorkspaceSkill()
