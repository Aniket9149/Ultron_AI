"""Central runtime configuration for ULTRON.

Values are read once from environment variables when ``Settings`` is created.
The display size remains lazy because importing configuration should not require
an active desktop session.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Final


DEFAULT_LM_STUDIO_BASE_URL: Final[str] = "http://localhost:1234/v1"
DEFAULT_LM_STUDIO_MODEL: Final[str] = "qwen2.5-coder-1.5b-instruct"
DEFAULT_WAKE_WORDS: Final[tuple[str, ...]] = ("ultron",)


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a number, got {value!r}") from exc
    if parsed < 0:
        raise ValueError(f"{name} must not be negative")
    return parsed


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {value!r}") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return parsed


@dataclass(frozen=True, slots=True)
class LatencyConfig:
    """Timing limits used by asynchronous runtime components."""

    bus_worker_count: int = field(default=4)
    session_vigilance_seconds: float = field(default=30.0)
    speech_timeout_seconds: float = field(default=5.0)
    command_timeout_seconds: float = field(default=30.0)


@dataclass(frozen=True, slots=True)
class Settings:
    """Single source of truth for environment and hardware-facing settings."""

    lm_studio_base_url: str = field(default=DEFAULT_LM_STUDIO_BASE_URL)
    lm_studio_model: str = field(default=DEFAULT_LM_STUDIO_MODEL)
    wake_words: tuple[str, ...] = field(default=DEFAULT_WAKE_WORDS)
    vocal_voice: str = field(default="hi-IN-MadhurNeural")
    display_resolution: tuple[int, int] | None = field(default=None)
    latency: LatencyConfig = field(default_factory=LatencyConfig)

    @property
    def lm_studio_chat_url(self) -> str:
        return f"{self.lm_studio_base_url.rstrip('/')}/chat/completions"

    @classmethod
    def from_environment(cls) -> "Settings":
        """Build settings from ``ULTRON_*`` environment overrides."""
        raw_wake_words = os.getenv("ULTRON_WAKE_WORDS", ",".join(DEFAULT_WAKE_WORDS))
        wake_words = tuple(word.strip().casefold() for word in raw_wake_words.split(",") if word.strip())
        if not wake_words:
            raise ValueError("ULTRON_WAKE_WORDS must contain at least one word")

        return cls(
            lm_studio_base_url=os.getenv("ULTRON_LM_STUDIO_BASE_URL", DEFAULT_LM_STUDIO_BASE_URL),
            lm_studio_model=os.getenv("ULTRON_LM_STUDIO_MODEL", DEFAULT_LM_STUDIO_MODEL),
            wake_words=wake_words,
            vocal_voice=os.getenv("ULTRON_VOCAL_VOICE", "hi-IN-MadhurNeural"),
            latency=LatencyConfig(
                bus_worker_count=_env_int("ULTRON_BUS_WORKER_COUNT", 4),
                session_vigilance_seconds=_env_float("ULTRON_SESSION_VIGILANCE_SECONDS", 30.0),
                speech_timeout_seconds=_env_float("ULTRON_SPEECH_TIMEOUT_SECONDS", 5.0),
                command_timeout_seconds=_env_float("ULTRON_COMMAND_TIMEOUT_SECONDS", 30.0),
            ),
        )

    def resolve_display_resolution(self) -> tuple[int, int]:
        """Return the configured size or query the active desktop via pyautogui."""
        if self.display_resolution is not None:
            return self.display_resolution

        try:
            import pyautogui
        except ImportError as exc:
            raise RuntimeError("pyautogui is required to query display resolution") from exc

        width, height = pyautogui.size()
        return int(width), int(height)


settings = Settings.from_environment()
