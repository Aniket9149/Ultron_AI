"""
03_Brain/user_manager.py
Persists user profile including active language configuration.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any

PROFILE_PATH = Path(__file__).resolve().parent / "user_profile.json"

def get_or_create_user(vocal_engine=None) -> Dict[str, Any]:
    if PROFILE_PATH.exists():
        try:
            with open(PROFILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "name" in data and "gender" in data:
                    if "language" not in data:
                        data["language"] = "hinglish"
                        with open(PROFILE_PATH, "w", encoding="utf-8") as fw:
                            json.dump(data, fw, indent=4)
                    return data
        except Exception:
            pass

    print("\n" + "="*60)
    print("[ONBOARDING]: Identify yourself to the Apex System.")
    print("="*60 + "\n")

    name = input("[Enter Your Name]: ").strip().capitalize() or "Aniket"
    gender = input("[Enter Gender (Male/Female)]: ").strip().lower()
    if gender not in ["male", "female", "boy", "girl"]:
        gender = "male"
    elif gender in ["boy"]:
        gender = "male"
    elif gender in ["girl"]:
        gender = "female"

    profile = {
        "name": name,
        "gender": gender,
        "language": "hinglish"  # Expandable for UI toggles: "english", "hinglish", "hindi"
    }

    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

    return profile
