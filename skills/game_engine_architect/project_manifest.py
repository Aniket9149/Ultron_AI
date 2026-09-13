"""
skills/game_engine_architect/project_manifest.py
Packages manifest and project configuration for Unity 6 (URP & Input System).
"""
import json
from pathlib import Path

MANIFEST_DATA = {
    "dependencies": {
        "com.unity.cinemachine": "3.1.2",
        "com.unity.inputsystem": "1.11.2",
        "com.unity.render-pipelines.universal": "17.0.3",
        "com.unity.textmeshpro": "3.2.0-pre.6",
        "com.unity.modules.ai": "1.0.0",
        "com.unity.modules.physics": "1.0.0",
        "com.unity.modules.terrain": "1.0.0",
        "com.unity.modules.ui": "1.0.0"
    }
}

def inject_project_manifest(project_path: Path):
    packages_dir = project_path / "Packages"
    packages_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = packages_dir / "manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(MANIFEST_DATA, f, indent=2)
