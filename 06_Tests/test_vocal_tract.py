"""Standalone verification for VocalTract bus delivery."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch


MODULE_PATH = Path(__file__).parents[1] / "06_Vocal" / "vocal_tract.py"
SPEC = importlib.util.spec_from_file_location("vocal_tract", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class VocalTractTests(unittest.TestCase):
    def test_impulse_payload_is_forwarded_to_engine(self) -> None:
        bus = MagicMock()
        engine = MagicMock()
        tract = MODULE.VocalTract(bus=bus, engine=engine)

        handler = bus.subscribe.call_args.args[1]
        impulse = MODULE.synapse_module.Impulse("VOCAL_IMPULSE", {"text": "Mujhe suno"})
        handler(impulse)

        engine.speak.assert_called_once_with("Mujhe suno")
        tract.close()
        bus.subscribe.return_value.cancel.assert_called_once_with()

    def test_empty_or_invalid_payload_is_ignored(self) -> None:
        bus = MagicMock()
        engine = MagicMock()
        tract = MODULE.VocalTract(bus=bus, engine=engine)
        handler = bus.subscribe.call_args.args[1]

        with patch.object(tract, "speak") as speak:
            handler(MODULE.synapse_module.Impulse("VOCAL_IMPULSE", {}))
            handler(MODULE.synapse_module.Impulse("VOCAL_IMPULSE", "not a mapping"))

        speak.assert_not_called()
        tract.close()


if __name__ == "__main__":
    unittest.main()