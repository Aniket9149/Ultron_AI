"""Strict context-aware TALK/TASK intent classification for ULTRON."""

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
TASK_ACTIONS = {
    "OPEN_APP", "CLOSE_APP", "CLOSE_WINDOW", "CLICK_UI", "INSPECT_SCREEN",
    "MOVE_CURSOR", "HOTKEY", "SCROLL", "MULTI_STEP_TASK",
}

SYSTEM_PROMPT = """You are Ultron's conversational and desktop-intent classifier.
Return exactly one JSON object and no markdown.
Classify the user's speech into one of these schemas:
TALK: {"type":"TALK","action":"CONVERSATION","reply":"concise natural 1-2 sentence Hinglish reply"}
TASK: {"type":"TASK","action":"OPEN_APP|CLOSE_WINDOW|CLICK_UI|INSPECT_SCREEN|MOVE_CURSOR|HOTKEY|SCROLL","target":"label or app, if applicable","reply":"short tactical Hinglish confirmation"}
TALK is mandatory for greetings, feelings, opinions, general knowledge, philosophical discussion, and questions about your abilities.
TASK is mandatory for explicit desktop actions or questions about current screen state.
Use MULTI_STEP_TASK for a request containing multiple ordered desktop actions; preserve the full request in target.
Never invent a TASK from casual conversation."""


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
    """Classify speech safely before producing any OS automation directive."""

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
            return self._talk_packet()

        normalized = user_text.casefold().strip()
        close_target = self._extract_close_target(normalized)
        if close_target is not None:
            return self._task_packet(
                "CLOSE_WINDOW",
                target=close_target,
                reply="Window band kar raha hoon.",
            )
        if self._looks_like_workflow(normalized):
            return self._task_packet("MULTI_STEP_TASK", target=user_text.strip(), reply="Kaam shuru kar raha hoon.")
        task_packet = self._fast_task_classification(normalized)
        if task_packet is not None:
            return task_packet

        llm_packet = self._ask_local_model(user_text)
        if llm_packet is not None:
            return self._normalize_llm_packet(llm_packet)
        return self._talk_packet()

    def _fast_task_classification(self, normalized: str) -> dict[str, Any] | None:
        if self._is_screen_inspection(normalized):
            return self._task_packet("INSPECT_SCREEN", reply="Screen inspect kar raha hoon.")

        if self.router is not None:
            cursor_packet = self.router.extract_cursor_intent(normalized)
            if cursor_packet:
                return self._task_packet(
                    "MOVE_CURSOR",
                    reply=f"Pointer ko {cursor_packet['zone']} par move kar raha hoon.",
                    x=cursor_packet.get("x"),
                    y=cursor_packet.get("y"),
                    zone=cursor_packet.get("zone"),
                )

        if self._has_any_token(normalized, ("hotkey", "shortcut", "minimize", "maximize", "restore")) or re.search(r"\b(?:ctrl|alt|win|shift)\s*\+?\s*[a-z0-9]\b", normalized):
            keys = self._extract_hotkey(normalized)
            return self._task_packet("HOTKEY", target="", reply="Keyboard shortcut chala raha hoon.", keys=keys)

        if self._has_any_token(normalized, ("scroll", "scrolling")):
            direction = "up" if self._has_any_token(normalized, ("upar", "up")) else "down"
            return self._task_packet("SCROLL", target=direction, reply=f"Screen ko {direction} scroll kar raha hoon.", direction=direction)

        if self._has_any_token(normalized, ("click", "dabao", "chuno", "select")):
            target = self._extract_target(normalized, {
                "click", "dabao", "chuno", "select", "karo", "karna", "par", "pe",
                "button", "use", "ko",
            })
            if target:
                return self._task_packet("CLICK_UI", target=target, reply=f"'{target}' par click kar raha hoon.")

        if self._has_any_token(normalized, ("open", "kholo", "chalao", "start", "launch")):
            target = self._extract_app_target(normalized)
            if target:
                return self._task_packet("OPEN_APP", target=target, reply=f"{target} open kar raha hoon.")
        return None

    @staticmethod
    def _looks_like_workflow(normalized: str) -> bool:
        has_action = any(word in normalized.split() for word in ("kholo", "open", "launch", "banao", "create", "type", "likho", "save", "click"))
        has_sequence = any(marker in normalized for marker in (" aur ", " and ", " phir ", " usme ", " then "))
        return has_action and has_sequence

    @staticmethod
    def _is_screen_inspection(normalized: str) -> bool:
        has_surface = any(term in normalized for term in ("screen", "desktop", "screen par", "screen pe"))
        has_question_or_action = any(term in normalized for term in ("kya", "dikh", "bata", "inspect", "check", "error", "dikhao"))
        return has_surface and has_question_or_action

    @staticmethod
    def _has_any_token(text: str, tokens: tuple[str, ...]) -> bool:
        words = set(re.findall(r"[\w']+", text))
        return any(token in words for token in tokens)

    @staticmethod
    def _extract_target(normalized: str, stop_words: set[str]) -> str:
        words = [word for word in re.findall(r"[\w']+", normalized) if word not in stop_words]
        return " ".join(words).strip()

    @staticmethod
    def _extract_app_target(normalized: str) -> str:
        match = re.search(r"(?:open|kholo|chalao|start|launch)\b(.*)$", normalized)
        if not match:
            return ""
        target = match.group(1).strip()
        target = re.sub(r"^(?:(?:karke|kar ke)\s+)?(?:dikhao|dikhado|please|zara)\s+", "", target)
        target = re.sub(r"\s+(?:kar|karo|karna|please)$", "", target).strip()
        if target in {"kar", "karo", "karna", "please"}:
            target = ""
        if not target:
            before = normalized[:match.start()].strip()
            target = before.split()[-1] if before else ""
        return target

    @staticmethod
    def _extract_close_target(normalized: str) -> str | None:
        trigger = re.search(r"\b(?:band\s+kar(?:o|na)?|close\s+(?:kar(?:o|na)?|do)?|hatao|exit\s+kar(?:o|na)?)\b", normalized)
        if not trigger:
            return None
        before = normalized[:trigger.start()].strip()
        before = re.sub(r"\b(?:mujhe|isko|is|window|app|please|zara)\b", " ", before)
        before = " ".join(before.split())
        return before or ""

    @staticmethod
    def _extract_hotkey(normalized: str) -> list[str]:
        match = re.search(r"\b(ctrl|alt|win|shift)\s*\+?\s*([a-z0-9])\b", normalized)
        if match:
            return [match.group(1), match.group(2)]
        if "close tab" in normalized or "band tab" in normalized:
            return ["ctrl", "w"]
        if "minimize" in normalized:
            return ["win", "down"]
        if "maximize" in normalized:
            return ["win", "up"]
        return []

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
        except Exception:
            return None

    @staticmethod
    def _normalize_llm_packet(packet: dict[str, Any]) -> dict[str, Any]:
        packet_type = packet.get("type")
        action = packet.get("action")
        reply = packet.get("reply", packet.get("response", "Main active hoon Aniket, agla command bolo."))
        if packet_type == "TASK" and action in TASK_ACTIONS:
            normalized = {"type": "TASK", "action": action, "target": packet.get("target", ""), "reply": reply}
            normalized.update({key: packet[key] for key in ("x", "y", "zone", "keys", "direction") if key in packet})
            return normalized
        return {"type": "TALK", "action": "CONVERSATION", "reply": reply}

    @staticmethod
    def _task_packet(action: str, target: str = "", reply: str = "", **extra: Any) -> dict[str, Any]:
        packet = {"type": "TASK", "action": action, "target": target, "reply": reply}
        packet.update({key: value for key, value in extra.items() if value is not None})
        return packet

    @staticmethod
    def _talk_packet(reply: str = "Main active hoon Aniket, agla command bolo.") -> dict[str, Any]:
        return {"type": "TALK", "action": "CONVERSATION", "reply": reply}


brain_engine = BrainEngine()
