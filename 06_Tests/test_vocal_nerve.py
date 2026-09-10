"""Live verification for the vocal impulse pipeline.

This script intentionally uses the real Edge-TTS/Pygame engine. Run it from
the repository root with an active desktop session and network access.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT_DIR = Path(__file__).parents[1]
VOCAL_TRACT_PATH = ROOT_DIR / "06_Vocal" / "vocal_tract.py"
SPEC = importlib.util.spec_from_file_location("ultron_vocal_tract", VOCAL_TRACT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {VOCAL_TRACT_PATH}")
VOCAL_MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VOCAL_MODULE)


def main() -> None:
    print("=== VERIFYING ULTRON VOCAL NERVE PIPELINE ===")
    synapse = VOCAL_MODULE.synapse
    if synapse is None:
        raise RuntimeError("SynapseBus could not be initialized")

    test_phrase = "Ultron vocal subsystem live ho chuka hai Aniket. Synapse nerve verified."
    print("[FIRING VOCAL IMPULSE OVER SYNAPSE BUS]...")
    futures = synapse.publish("VOCAL_IMPULSE", {"text": test_phrase})
    for future in futures:
        future.result()
    print("[TEST COMPLETE]")


if __name__ == "__main__":
    main()