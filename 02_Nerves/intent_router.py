"""
02_Nerves/intent_router.py
Robust Intent Router with Open & Close Process Controls.
"""
from __future__ import annotations
import re
from typing import Dict, Any, Optional
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent.parent

a_spec = importlib.util.spec_from_file_location("system_actuator", ROOT / "02_Nerves" / "system_actuator.py")
a_mod = importlib.util.module_from_spec(a_spec)
a_spec.loader.exec_module(a_mod)
actuator = a_mod.actuator

class IntentRouter:
    def route_and_execute(self, raw_text: str) -> Optional[Dict[str, Any]]:
        clean = re.sub(r"[^\w\s]", "", raw_text.lower()).strip()
        clean = re.sub(r"^\bultron\b\s*", "", clean).strip()

        # 1. Close / Kill Actions (Highest Priority)
        close_match = re.search(r"\b(?:close|kill|band karo|hatao|exit)\s+(.+)", clean)
        if close_match:
            target_to_close = close_match.group(1).strip()
            actuator.close_application(target_to_close)
            return {"action": "close_app", "detail": target_to_close}

        # 2. Volume Controls
        if any(v in clean for v in ["volume up", "sound badhao", "awaz badhao"]):
            actuator.volume_up()
            return {"action": "volume_up", "detail": "Volume Increased"}

        if any(v in clean for v in ["volume down", "sound kam", "awaz kam"]):
            actuator.volume_down()
            return {"action": "volume_down", "detail": "Volume Decreased"}

        if any(v in clean for v in ["mute", "awaz band", "chup"]):
            actuator.volume_mute()
            return {"action": "mute", "detail": "Muted"}

        # 3. YouTube
        if "youtube" in clean:
            query = re.sub(r"\b(open|search|play|kholo|chalao|on|pe|par|youtube)\b", "", clean).strip()
            if query:
                actuator.search_youtube(query)
                return {"action": "youtube_search", "detail": query}
            else:
                actuator.open_url("youtube.com")
                return {"action": "open_url", "detail": "YouTube"}

        # 4. Google
        if "google" in clean or clean.startswith("search"):
            query = re.sub(r"\b(search|on|google|par|karo|find)\b", "", clean).strip()
            if query:
                actuator.search_google(query)
                return {"action": "google_search", "detail": query}

        # 5. Open Any App
        open_match = re.search(r"\b(?:open|launch|kholo|start)\s+(.+)", clean)
        if open_match:
            app_target = open_match.group(1).strip()
            if app_target not in ["mouth", "eyes", "window"]:
                actuator.open_application(app_target)
                return {"action": "open_app", "detail": app_target}

        # 6. Screenshot
        if "screenshot" in clean:
            shot_file = actuator.take_screenshot()
            return {"action": "screenshot", "detail": shot_file}

        return None

intent_router = IntentRouter()
