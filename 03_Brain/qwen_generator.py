"""
03_Brain/qwen_generator.py
Stateful Autonomous Brain with Multi-Turn File and Folder Conflict Management.
Supports: .py, .txt, .json, and generic extensions with Overwrite/Rename/Cancel state.
"""
from __future__ import annotations
import re
import sys
import os
import json
import requests
import subprocess
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

autonomous_core = import_module("05_Actions.autonomous_core").autonomous_core
pending_store = import_module("01_Memory.pending_actions").pending_store

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_ID = "qwen2.5-coder-1.5b-instruct"

def get_desktop_dir() -> Path:
    res = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
        capture_output=True,
        text=True
    )
    p = res.stdout.strip()
    if p:
        return Path(p)
    return Path(os.environ.get("USERPROFILE", ".")) / "Desktop"

def handle_pending_resolution(user_text: str, pending: dict) -> str:
    cmd = user_text.lower().strip()
    target_path = Path(pending["path"])
    item_type = pending.get("type", "item")
    name = target_path.name
    parent = target_path.parent
    content = pending.get("context", {}).get("content", "")

    # 1. REPLACE / OVERWRITE
    if any(w in cmd for w in ["replace", "overwrite", "badal", "hata ke", "purana delete"]):
        if item_type == "create_folder":
            ps = f'Remove-Item -Path "{target_path}" -Recurse -Force -ErrorAction SilentlyContinue; New-Item -ItemType Directory -Path "{target_path}" -Force | Out-Null'
            autonomous_core.execute_powershell(ps)
        else:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
        pending_store.clear()
        return f"Purana '{name}' replace kar diya fresh content ke saath."

    # 2. RENAME / AUTO INCREMENT
    if any(w in cmd for w in ["rename", "naam", "change", "dusra", "alag", "naya"]):
        stem = target_path.stem
        suffix = target_path.suffix
        idx = 1
        new_path = parent / f"{stem}_{idx}{suffix}"
        while new_path.exists():
            idx += 1
            new_path = parent / f"{stem}_{idx}{suffix}"

        if item_type == "create_folder":
            ps = f'New-Item -ItemType Directory -Path "{new_path}" -Force | Out-Null'
            autonomous_core.execute_powershell(ps)
        else:
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(content)

        pending_store.clear()
        return f"Done! Conflict avoid karne ke liye '{new_path.name}' bana di."

    # 3. CANCEL
    if any(w in cmd for w in ["cancel", "rehne de", "chhod", "mat bana", "ruk"]):
        pending_store.clear()
        return f"Theek hai, plan drop. '{name}' ko chheda bhi nahi."

    return f"Saaf bol: '{name}' ko 'replace' karna hai, 'rename' karna hai, ya 'cancel'?"

def generate_and_execute(user_text: str) -> str:
    if not user_text.strip():
        return ""

    # Check pending resolution
    pending = pending_store.get_pending()
    if pending:
        return handle_pending_resolution(user_text, pending)

    desktop = get_desktop_dir()

    # --- INTENT 1: FILE CREATION (.py, .txt, .json, etc.) ---
    file_match = re.search(r'(?:file\s*bana|create\s*file|file\s*save|save\s*file)\s*([a-zA-Z0-9_\-\.\s]*)', user_text, re.IGNORECASE)
    if file_match:
        raw_name = file_match.group(1).strip() or "notes.txt"
        # Auto-append .txt if no extension specified
        if "." not in raw_name:
            raw_name += ".txt"

        target_file = desktop / raw_name

        # Detect conflict
        if target_file.exists():
            pending_store.set_pending("create_file", str(target_file), {"content": ""})
            return f"Ruk! '{raw_name}' file Desktop pe pehle se maujood hai. Bol kya karun—'replace' karun, 'rename' karun, ya 'cancel'?"

        # Safe Create
        with open(target_file, "w", encoding="utf-8") as f:
            f.write("")
        return f"Desktop par '{raw_name}' file create kar di."

    # --- INTENT 2: FOLDER CREATION ---
    folder_match = re.search(r'(?:folder\s*bana|create\s*folder|naya\s*folder)\s*([a-zA-Z0-9_\-\s]*)', user_text, re.IGNORECASE)
    if folder_match:
        folder_name = folder_match.group(1).strip() or "New_Folder"
        target_folder = desktop / folder_name

        if target_folder.exists():
            pending_store.set_pending("create_folder", str(target_folder))
            return f"Ruk! '{folder_name}' folder Desktop pe pehle se bana hua hai. Bol kya karun—'replace' karun, 'rename' karun, ya 'cancel'?"

        ps = f'New-Item -ItemType Directory -Path "{target_folder}" -Force | Out-Null'
        autonomous_core.execute_powershell(ps)
        return f"Desktop par '{folder_name}' folder bana diya."

    # --- LLM FALLBACK ---
    payload = {
        "model": MODEL_ID,
        "messages": [
            {"role": "system", "content": "You are ULTRON, a ruthless AI controlling Windows PC. Respond in 1 short Hinglish line."},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.2,
        "max_tokens": 80
    }

    try:
        res = requests.post(LM_STUDIO_URL, json=payload, timeout=15)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].replace('"', '').strip()
        return "Task process nahi hua."
    except Exception as exc:
        return f"[BRAIN_ERROR]: {exc}"
