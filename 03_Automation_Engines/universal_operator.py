"""Generic Windows application discovery and UI-grounded operation."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys
import subprocess
import time
from typing import Any

import pyautogui
import pygetwindow as gw


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


def _load_module(module_name: str, path: Path) -> Any | None:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        return None
    return module


uia_module = _load_module("ultron_operator_native_grounding", ROOT_DIR / "01_Sense" / "native_grounding.py")
spine_module = _load_module("ultron_operator_reflex_planner", ROOT_DIR / "04_Spine" / "reflex_planner.py")
uia = getattr(uia_module, "native_grounding", None)
synapse = getattr(spine_module, "synapse", None)
catalog_module = _load_module("ultron_operator_system_catalog", ROOT_DIR / "01_Sense" / "system_catalog.py")
system_catalog = getattr(catalog_module, "system_catalog", None)


class UniversalOperator:
    """Discover applications and dispatch grounded UI actions."""

    def __init__(
        self,
        ui_grounding: Any | None = None,
        bus: Any | None = None,
        window_api: Any = gw,
        input_api: Any = pyautogui,
        app_catalog: Any | None = None,
    ) -> None:
        self.ui_grounding = ui_grounding if ui_grounding is not None else uia
        self.bus = bus if bus is not None else synapse
        self.window_api = window_api
        self.input_api = input_api
        self.app_catalog = app_catalog if app_catalog is not None else system_catalog

    def open_any_app(self, app_name: str) -> bool | dict[str, str]:
        """Focus a running app or launch a locally verified app without web search."""
        target = app_name.strip().casefold()
        if not target:
            return False

        for window in self.window_api.getAllWindows():
            title = getattr(window, "title", "")
            if target in title.casefold() and title.strip():
                try:
                    if getattr(window, "isMinimized", False):
                        window.restore()
                    window.activate()
                    time.sleep(0.3)
                    print(f"[OPERATOR]: Focused existing window '{title}'")
                    return True
                except Exception:
                    continue

        installed, path = self.app_catalog.is_app_installed(app_name) if self.app_catalog is not None else (False, "")
        if not installed:
            prompt = f"'{app_name}' aapke PC me installed nahi hai. Kya aap chahte hain ki main ise download ya install karoon?"
            print(f"[OPERATOR]: {prompt}")
            return {"success": False, "status": "NOT_INSTALLED", "prompt": prompt}

        print(f"[OPERATOR]: Launching locally verified app '{app_name}' from '{path}'")
        if path.casefold().endswith((".lnk", ".url")):
            os.startfile(path)
        else:
            subprocess.Popen([path])
        return True

    def close_window(self, target: str = "") -> bool:
        """Close a matching window, or the current foreground window when empty."""
        target_folded = target.strip().casefold()
        windows = self.window_api.getAllWindows()
        selected = None
        if target_folded:
            selected = next(
                (
                    window for window in windows
                    if target_folded in str(getattr(window, "title", "")).casefold()
                ),
                None,
            )
        else:
            active = getattr(self.window_api, "getActiveWindow", lambda: None)()
            selected = active
        if selected is not None:
            try:
                selected.close()
                return True
            except Exception:
                return False
        self.input_api.hotkey("alt", "f4")
        return True

    def click_element(self, element_query: str) -> bool:
        """Ground an element and publish a click directive to the motor bus."""
        clean_target = element_query.strip()
        if not clean_target or self.ui_grounding is None or self.bus is None:
            return False

        if any(label in clean_target.casefold() for label in ("new tab", "plus", "tab")):
            coordinates = self.ui_grounding.get_new_tab_button()
        else:
            coordinates = self.ui_grounding.locate_active_text(clean_target)

        if not coordinates:
            print(f"[OPERATOR]: Element '{clean_target}' not found in active UI tree.")
            return False

        print(f"[OPERATOR]: Target '{clean_target}' confirmed at {coordinates}. Dispatching click...")
        futures = self.bus.publish(
            "MOTOR_DIRECTIVE",
            {
                "action": "CLICK_COORDS",
                "data": {"x": coordinates[0], "y": coordinates[1]},
            },
        )
        for future in futures:
            future.result()
        return True


universal_operator = UniversalOperator()