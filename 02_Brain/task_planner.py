"""Decompose high-level desktop requests into atomic workflow steps."""

from __future__ import annotations

import json
import re
from typing import Any

import requests


TASK_PRIMITIVES = {"LAUNCH", "SHELL_EXEC", "GUI_CLICK", "KEYSTROKE", "WAIT"}
PLANNER_SYSTEM_PROMPT = """You are Ultron's desktop workflow planner.
Convert a user's OS request into a JSON array of ordered atomic steps.
Allowed primitives only: LAUNCH, SHELL_EXEC, GUI_CLICK, KEYSTROKE, WAIT.
Each step must contain an integer step and primitive. Use executable targets,
short waits, UI labels, keyboard actions, or safe PowerShell commands.
Never invent application-specific APIs or hidden coordinates. Return JSON only."""


class TaskPlanner:
    """Plan generalized workflows with local structured reasoning and fallback parsing."""

    def __init__(
        self,
        http_client: Any = requests,
        endpoint: str = "http://localhost:1234/v1/chat/completions",
        model: str = "qwen2.5-coder-1.5b-instruct",
        timeout: float = 6.0,
    ) -> None:
        self.http_client = http_client
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout

    def plan(self, command: str) -> list[dict[str, Any]]:
        if not isinstance(command, str) or not command.strip():
            return []
        generated = self._ask_model(command)
        if generated:
            return self._validate_steps(generated)
        return self._fallback_plan(command.strip())

    def _ask_model(self, command: str) -> list[dict[str, Any]] | None:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                {"role": "user", "content": command},
            ],
            "temperature": 0.1,
        }
        try:
            response = self.http_client.post(self.endpoint, json=payload, timeout=self.timeout)
            if response.status_code != 200:
                return None
            content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            match = re.search(r"\[.*\]", content.strip(), re.DOTALL)
            decoded = json.loads(match.group(0)) if match else None
            return decoded if isinstance(decoded, list) else None
        except Exception:
            return None

    @staticmethod
    def _validate_steps(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
        valid: list[dict[str, Any]] = []
        for index, raw_step in enumerate(steps, start=1):
            if not isinstance(raw_step, dict) or raw_step.get("primitive") not in TASK_PRIMITIVES:
                continue
            step = dict(raw_step)
            step["step"] = index
            valid.append(step)
        return valid

    @staticmethod
    def _fallback_plan(command: str) -> list[dict[str, Any]]:
        normalized = command.casefold()
        steps: list[dict[str, Any]] = []
        launch_match = re.search(
            r"(?:^|\b(?:aur|and|then|phir)\b)\s*([\w .-]+?)\s+(?:kholo|open|launch|start)\b",
            command,
            re.IGNORECASE,
        )
        if launch_match is None:
            launch_match = re.search(
                r"\b(?:kholo|open|launch|start)\s+([\w .-]+)", command, re.IGNORECASE
            )
        if launch_match is None:
            launch_match = re.search(
                r"\b([\w .-]+?)\s+(?:me\s+)?(?:jakar|jake|jao)\b",
                command,
                re.IGNORECASE,
            )
        if launch_match:
            target = launch_match.group(1).strip(" .,!?\n")
            steps.extend((
                {"primitive": "LAUNCH", "target": target},
                {"primitive": "WAIT", "duration": 1.0},
            ))

        if any(word in normalized for word in ("folder", "directory")) and any(word in normalized for word in ("banao", "create", "make")):
            folder_match = re.search(
                r"([\w.-]+)\s+(?:naam\s+ka|named)\s+(?:folder|directory)"
                r"|(?:folder|directory)\s+(?:naam\s+se\s+|named\s+|name\s+)?([\w.-]+)",
                command, re.IGNORECASE,
            )
            folder_name = next((group for group in (folder_match.groups() if folder_match else ()) if group), "New Folder")
            steps.extend((
                {"primitive": "KEYSTROKE", "action": "HOTKEY", "keys": ["ctrl", "shift", "n"]},
                {"primitive": "KEYSTROKE", "action": "TYPE", "text": folder_name, "press_enter": True},
            ))

        if any(word in normalized for word in ("type", "likho", "write", "note")):
            text_match = re.search(r"(?:type|likho|write|note)\s+(?:that\s+)?(.+?)(?:\s+and\s+save|\s+save|$)", command, re.IGNORECASE)
            text = text_match.group(1).strip() if text_match else ""
            if text:
                steps.append({"primitive": "KEYSTROKE", "action": "TYPE", "text": text, "press_enter": False})
            if "save" in normalized:
                steps.append({"primitive": "KEYSTROKE", "action": "HOTKEY", "keys": ["ctrl", "s"]})
            if any(word in normalized for word in ("close", "band", "exit")):
                steps.append({"primitive": "KEYSTROKE", "action": "HOTKEY", "keys": ["alt", "f4"]})

        click_match = re.search(r"(?:click|dabao|select)\s+(.+?)(?:\s+and\s+|$)", command, re.IGNORECASE)
        if click_match:
            steps.append({"primitive": "GUI_CLICK", "target": click_match.group(1).strip()})
        elif any(word in normalized for word in ("check", "inspect", "dekho", "batao")):
            preceding_check = re.search(
                r"\b([\w .-]+?)\s+(?:check|inspect|dekho|batao)\b",
                command,
                re.IGNORECASE,
            )
            if preceding_check:
                target = re.split(
                    r"\b(?:me\s+jakar|me|par)\b",
                    preceding_check.group(1),
                    maxsplit=1,
                    flags=re.IGNORECASE,
                )[-1].strip()
                if target:
                    steps.append({"primitive": "GUI_CLICK", "target": target})
                    return TaskPlanner._renumber(steps)
            check_match = re.search(
                r"(?:check|inspect|dekho|batao)\s+(?:the\s+|is\s+)?([\w .-]+)",
                command,
                re.IGNORECASE,
            )
            if check_match:
                target = re.sub(r"\s+(?:karo|karna|please)$", "", check_match.group(1).strip(), flags=re.IGNORECASE)
                if target:
                    steps.append({"primitive": "GUI_CLICK", "target": target})

        return TaskPlanner._renumber(steps)

    @staticmethod
    def _renumber(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
        for index, step in enumerate(steps, start=1):
            step["step"] = index
        return steps


task_planner = TaskPlanner()
