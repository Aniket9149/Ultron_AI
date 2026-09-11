"""
02_Nerves/synapse_bus.py
Layer 4: Unified clean access node orchestrating layers 1 to 3.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
from typing import Any, Callable, Dict, Optional

MODULE_ROOT = Path(__file__).resolve().parent


def _import_local(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_filter_mod = _import_local("telemetry_filter", MODULE_ROOT / "telemetry_filter.py")
_router_mod = _import_local("event_router", MODULE_ROOT / "event_router.py")
_executor_mod = _import_local("nerve_executor", MODULE_ROOT / "nerve_executor.py")

TelemetryFilter = _filter_mod.TelemetryFilter
EventRouter = _router_mod.EventRouter
NerveExecutor = _executor_mod.NerveExecutor


class SynapseBus:
    """The 4-stage filtered nervous routing core for Ultron."""

    def __init__(self, worker_count: int = 6) -> None:
        self.router = EventRouter()
        self.executor = NerveExecutor(worker_count=worker_count)

    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        self.router.register(topic, handler)

    def publish(self, topic: str, payload: Optional[Dict[str, Any]] = None) -> bool:
        clean_payload = TelemetryFilter.sanitize(topic, payload)
        if clean_payload is None:
            return False

        handlers = self.router.resolve_handlers(topic)
        if not handlers:
            return False

        priority = self.router.classify_priority(topic)
        for handler in handlers:
            self.executor.submit(priority, handler, clean_payload)
        return True

    def shutdown(self, wait: bool = False) -> None:
        self.executor.shutdown(wait=wait)
