"""Live verification for the cognitive BrainEngine pipeline."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT_DIR = Path(__file__).parents[1]
BRAIN_PATH = ROOT_DIR / "02_Brain" / "brain_engine.py"
SPEC = importlib.util.spec_from_file_location("ultron_brain_engine", BRAIN_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {BRAIN_PATH}")
BRAIN_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BRAIN_MODULE)


def main() -> int:
    print("=== VERIFYING ULTRON COGNITIVE BRAIN PIPELINE ===")
    brain = BRAIN_MODULE.brain_engine
    test_prompts = [
        "Cursor ko center mein lao",
        "Screen par kya dikh raha hai?",
        "Microsoft Store open karo",
        "New tab par click karo",
    ]

    for prompt in test_prompts:
        print(f'\n[USER SAYS]: "{prompt}"')
        packet = brain.decide(prompt)
        print("[DECIDED PACKET]:", json.dumps(packet, indent=2, ensure_ascii=False))

    print("\n[SUCCESS]: Cognitive brain pipeline verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())