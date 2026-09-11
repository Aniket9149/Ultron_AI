"""Standalone checks for local app discovery and sanitized app intents."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch


ROOT_DIR = Path(__file__).parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CATALOG_MODULE = load_module("system_catalog_test_module", ROOT_DIR / "01_Sense" / "system_catalog.py")
BRAIN_MODULE = load_module("system_catalog_brain_test_module", ROOT_DIR / "02_Brain" / "brain_engine.py")
OPERATOR_MODULE = load_module("system_catalog_operator_test_module", ROOT_DIR / "03_Automation_Engines" / "universal_operator.py")


class SystemCatalogTests(unittest.TestCase):
    def test_installed_notepad_resolves_locally(self) -> None:
        installed, path = CATALOG_MODULE.SystemCatalog().is_app_installed("notepad")
        self.assertTrue(installed)
        self.assertTrue(path)

    def test_fake_app_is_rejected_without_windows_search(self) -> None:
        catalog = CATALOG_MODULE.SystemCatalog(scan=False)
        operator = OPERATOR_MODULE.UniversalOperator(
            ui_grounding=MagicMock(),
            bus=MagicMock(),
            window_api=MagicMock(getAllWindows=MagicMock(return_value=[])),
            input_api=MagicMock(),
            app_catalog=catalog,
        )

        result = operator.open_any_app("random_fake_app_xyz")

        self.assertFalse(result["success"])
        self.assertEqual(result["status"], "NOT_INSTALLED")
        operator.input_api.press.assert_not_called()
        operator.input_api.write.assert_not_called()

    def test_noisy_open_phrase_extracts_only_application_name(self) -> None:
        engine = BRAIN_MODULE.BrainEngine(http_client=MagicMock(), router=MagicMock())
        engine.router.extract_cursor_intent.return_value = None

        packet = engine.decide(
            "mujhe iska pata nahi lag raha isko open karke dikhao visual studio code"
        )

        self.assertEqual(packet["action"], "OPEN_APP")
        self.assertEqual(packet["target"], "visual studio code")

    def test_close_phrase_produces_close_window_action(self) -> None:
        engine = BRAIN_MODULE.BrainEngine(http_client=MagicMock(), router=MagicMock())
        engine.router.extract_cursor_intent.return_value = None

        packet = engine.decide("notepad band kar do")

        self.assertEqual(packet["action"], "CLOSE_WINDOW")
        self.assertEqual(packet["target"], "notepad")


if __name__ == "__main__":
    unittest.main()
