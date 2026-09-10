"""Standalone verification for the SynapseBus milestone."""

from __future__ import annotations

import importlib.util
import sys
import threading
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).parents[1] / "02_Nerves" / "synapse_bus.py"
SPEC = importlib.util.spec_from_file_location("synapse_bus", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["synapse_bus"] = MODULE
SPEC.loader.exec_module(MODULE)

Impulse = MODULE.Impulse
SynapseBus = MODULE.SynapseBus


class SynapseBusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.bus = SynapseBus(worker_count=2)
        self.received: list[Impulse] = []
        self.received_event = threading.Event()

    def tearDown(self) -> None:
        self.bus.close()
        SynapseBus._instance = None

    def test_singleton_and_async_delivery(self) -> None:
        self.assertIs(self.bus, SynapseBus())

        def handler(impulse: Impulse) -> None:
            self.received.append(impulse)
            self.received_event.set()

        subscription = self.bus.subscribe(" sensory_heard ", handler)
        futures = self.bus.publish("SENSORY_HEARD", {"text": "hello"})

        self.assertEqual(len(futures), 1)
        self.assertTrue(self.received_event.wait(timeout=1))
        futures[0].result(timeout=1)
        self.assertEqual(self.received[0].topic, "SENSORY_HEARD")
        self.assertEqual(self.received[0].payload, {"text": "hello"})
        self.assertIsNotNone(self.received[0].occurred_at)

        subscription.cancel()
        self.assertEqual(self.bus.publish("SENSORY_HEARD"), ())

    def test_invalid_topics_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.bus.subscribe("", lambda _: None)
        with self.assertRaises(ValueError):
            self.bus.publish("   ")


if __name__ == "__main__":
    unittest.main()
