"""Live verification for the UniversalOperator pipeline.

Run manually from the repository root. This may focus or launch an application
and may physically click a grounded UI element.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT_DIR = Path(__file__).parents[1]
OPERATOR_PATH = ROOT_DIR / "03_Automation_Engines" / "universal_operator.py"
SPEC = importlib.util.spec_from_file_location("ultron_universal_operator", OPERATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {OPERATOR_PATH}")
OPERATOR_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OPERATOR_MODULE)


def main() -> int:
    print("=== VERIFYING UNIVERSAL OPERATOR PIPELINE ===")
    operator = OPERATOR_MODULE.universal_operator

    print("\n1. Testing Generic Application Focus (Brave)...")
    if not operator.open_any_app("Brave"):
        print("[WARNING]: Application focus or launch failed.")
        return 1

    print("\n2. Testing Dynamic Element Grounding & Physical Click (New Tab)...")
    success = operator.click_element("new tab")
    if success:
        print("\n[SUCCESS]: Element resolved and click directive completed.")
        return 0

    print("\n[WARNING]: UI element lookup missed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())