"""
02_Nerves/nerve_executor.py
Layer 3: Priority-driven isolated worker pool preventing engine bottlenecks.
"""
from __future__ import annotations
import queue
import threading
from typing import Any, Callable, Dict, Optional


class NerveExecutor:
    def __init__(self, worker_count: int = 6) -> None:
        self._queue: queue.PriorityQueue[tuple[int, int, Callable[[Dict[str, Any]], Any], Dict[str, Any]]] = queue.PriorityQueue()
        self._workers: list[threading.Thread] = []
        self._running = True
        self._counter = 0
        self._lock = threading.Lock()

        for index in range(worker_count):
            worker = threading.Thread(
                target=self._worker_loop,
                daemon=True,
                name=f"SynapseFiltrationWorker-{index + 1}"
            )
            worker.start()
            self._workers.append(worker)

    def submit(self, priority: int, handler: Callable[[Dict[str, Any]], Any], payload: Dict[str, Any]) -> None:
        if not self._running:
            return
        with self._lock:
            self._counter += 1
            order = self._counter
        self._queue.put((priority, order, handler, payload))

    def _worker_loop(self) -> None:
        while self._running:
            try:
                priority, order, handler, payload = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue

            try:
                handler(payload)
            except Exception as exc:
                print(f"[SYNAPSE_NERVE_EXCEPTION]: {exc}")
            finally:
                self._queue.task_done()

    def shutdown(self, wait: bool = False) -> None:
        self._running = False
        if wait:
            for worker in self._workers:
                worker.join(timeout=1.0)
