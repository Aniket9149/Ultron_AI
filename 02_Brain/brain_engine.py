"""Local LM Studio reasoning and tactical intent decomposition."""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from typing import Any

import requests


BASE_DIR = Path(__file__).resolve().parent
ROUTER_PATH = BASE_DIR / "cursor_router.py"
LM_STUDIO_URL = os.getenv("ULTRON_LM_STUDIO_CHAT_URL", "http://localhost:1234/v1/chat/completions")
MODEL_NAME = os.getenv("ULTRON_LM_STUDIO_MODEL", "qwen2.5-coder-1.5b-instruct")

SYSTEM_PROMPT = """You are Ultron, an autonomous OS automation brain.
Analyze the user's spoken command and generate a single tactical execution JSON packet.
Available Actions:
1. OPEN_APP: open or focus an application. Include target and a short response.
2. CLICK_UI: click an on-screen element. Include target and a short response.
3. INSPECT_SCREEN: inspect visible windows. Use empty target and response.
4. HOTKEY: dispatch a keyboard shortcut. Include keys and a short response.
5. CHAT: answer general conversation. Include a short response.

Return only the raw JSON object without markdown fences or additional explanation."""


def _load_cursor_router() -> Any | None:
    spec = importlib.util.spec_from_file_location("ultron_cursor_router", ROUTER_PATH)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ultron_cursor_router"] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return module


cursor_router = _load_cursor_router()


class BrainEngine:
    """Resolve commands through reflexes, LM Studio, then safe heuristics."""

    def __init__(
        self,
        http_client: Any = requests,
        router: Any | None = cursor_router,
        endpoint: str = LM_STUDIO_URL,
        model: str = MODEL_NAME,
        timeout: float = 6.0,
    ) -> None:
        self.http_client = http_client
        self.router = router
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout

    def decide(self, user_text: str) -> dict[str, Any]:
        if not isinstance(user_text, str) or not user_text.strip():
            return self._chat_fallback()

        normalized = user_text.casefold().strip()
        if any(word in normalized for word in ("screen", "desktop")) and any(
            word in normalized for word in ("kya", "dikh", "batao", "open")
        ):
            return {"action": "INSPECT_SCREEN", "target": "", "response": ""}

        if self.router is not None:
            cursor_packet = self.router.extract_cursor_intent(normalized)
            if cursor_packet:
                cursor_packet["response"] = f"Pointer ko {cursor_packet['zone']} par move kar diya."
                return cursor_packet

        click_target = self._extract_click_target(normalized)
        if click_target:
            return {
                "action": "CLICK_UI",
                "target": click_target,
                "response": f"'{click_target}' par click kar raha hoon.",
            }

        llm_packet = self._ask_local_model(user_text)
        if llm_packet is not None:
            return llm_packet
        return self._heuristic_fallback(normalized)

    @staticmethod
    def _extract_click_target(normalized: str) -> str:
        if not any(word in normalized.split() for word in ("click", "dabao", "chuno", "select")):
            return ""
        stop_words = {
            "click", "dabao", "chuno", "select", "karo", "karna", "par", "pe",
            "button", "use", "ko",
        }
        target_words = [
            word for word in re.findall(r"[\w']+", normalized)
            if word not in stop_words
        ]
        return " ".join(target_words).strip()

    def _ask_local_model(self, user_text: str) -> dict[str, Any] | None:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            "temperature": 0.1,
        }
        try:
            response = self.http_client.post(self.endpoint, json=payload, timeout=self.timeout)
            if response.status_code != 200:
                return None
            raw = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            match = re.search(r"\{.*\}", raw.strip(), re.DOTALL)
            if not match:
                return None
            packet = json.loads(match.group(0))
            return packet if isinstance(packet, dict) else None
        except (AttributeError, IndexError, KeyError, TypeError, ValueError, requests.RequestException):
            return None
        except Exception:
            return None

    @staticmethod
    def _heuristic_fallback(normalized: str) -> dict[str, Any]:
        if any(word in normalized.split() for word in ("open", "kholo", "chalao", "start")):
            app_name = re.sub(
                r"\b(open|kholo|chalao|start|karo|zara|bhai)\b",
                "",
                normalized,
            ).strip()
            if app_name:
                return {
                    "action": "OPEN_APP",
                    "target": app_name,
                    "response": f"{app_name} open kar raha hoon.",
                }
        return BrainEngine._chat_fallback()

    @staticmethod
    def _chat_fallback() -> dict[str, Any]:
        return {
            "action": "CHAT",
            "target": "",
            "response": "Main active hoon Aniket, agla command bolo.",
        }


brain_engine = BrainEngine()
