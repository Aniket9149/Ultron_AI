"""Thread-safe asynchronous Pub/Sub transport for ULTRON modules."""

from __future__ import annotations

import threading
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, ClassVar


ImpulseHandler = Callable[["Impulse"], Any]


@dataclass(frozen=True, slots=True)
class Impulse:
    """An immutable message travelling across the nervous system."""

    topic: str
    payload: Any = None
    occurred_at: datetime = datetime.min.replace(tzinfo=timezone.utc)


class Subscription:
    """A cancellable registration returned by :meth:`SynapseBus.subscribe`."""

    def __init__(self, bus: "SynapseBus", topic: str, handler: ImpulseHandler) -> None:
        self._bus = bus
        self.topic = topic
        self.handler = handler
        self._cancelled = False
        self._lock = threading.Lock()

    def cancel(self) -> None:
        with self._lock:
            if self._cancelled:
                return
            self._cancelled = True
        self._bus.unsubscribe(self)

    @property
    def cancelled(self) -> bool:
        with self._lock:
            return self._cancelled


class SynapseBus:
    """Singleton event bus with non-blocking producer-side publication."""

    _instance: ClassVar["SynapseBus | None"] = None
    _instance_lock: ClassVar[threading.Lock] = threading.Lock()

    def __new__(cls, worker_count: int = 4) -> "SynapseBus":
        with cls._instance_lock:
            if cls._instance is None:
                instance = super().__new__(cls)
                instance._initialize(worker_count)
                cls._instance = instance
            return cls._instance

    def _initialize(self, worker_count: int) -> None:
        if worker_count <= 0:
            raise ValueError("worker_count must be greater than zero")
        self._subscriptions: dict[str, list[Subscription]] = {}
        self._lock = threading.RLock()
        self._executor = ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix="ultron-synapse")

    def subscribe(self, topic: str, handler: ImpulseHandler) -> Subscription:
        """Register a handler and return a token that can later be cancelled."""
        normalized_topic = self._validate_topic(topic)
        subscription = Subscription(self, normalized_topic, handler)
        with self._lock:
            self._subscriptions.setdefault(normalized_topic, []).append(subscription)
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove a subscription without affecting other handlers."""
        with self._lock:
            handlers = self._subscriptions.get(subscription.topic, [])
            self._subscriptions[subscription.topic] = [
                item for item in handlers if item is not subscription
            ]
            if not self._subscriptions[subscription.topic]:
                del self._subscriptions[subscription.topic]

    def publish(self, topic: str, payload: Any = None) -> tuple[Future[Any], ...]:
        """Queue an impulse for every current subscriber and return its futures."""
        normalized_topic = self._validate_topic(topic)
        impulse = Impulse(
            topic=normalized_topic,
            payload=payload,
            occurred_at=datetime.now(timezone.utc),
        )
        with self._lock:
            handlers = tuple(self._subscriptions.get(normalized_topic, ()))
        return tuple(
            self._executor.submit(subscription.handler, impulse)
            for subscription in handlers
            if not subscription.cancelled
        )

    def close(self, wait: bool = True) -> None:
        """Stop worker threads after queued handlers complete by default."""
        self._executor.shutdown(wait=wait)

    @staticmethod
    def _validate_topic(topic: str) -> str:
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("topic must be a non-empty string")
        return topic.strip().upper()
