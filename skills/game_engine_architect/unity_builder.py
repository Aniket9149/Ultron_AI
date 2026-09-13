"""
unity_builder.py
Enterprise Unity Workspace Scaffolder & Pipeline Automator.
"""
from __future__ import annotations
import sys
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

stream_writer = import_module("skills.stream_writer").stream_writer
banter_engine = import_module("skills.banter_engine").banter_engine
workspace = import_module("skills.workspace_tools").workspace
templates = import_module("skills.game_engine_architect.csharp_templates")

COMMERCIAL_PROJECT_LAYOUT = [
    "Assets/_Game/Scripts/Core",
    "Assets/_Game/Scripts/Player",
    "Assets/_Game/Scripts/AI",
    "Assets/_Game/Scripts/UI",
    "Assets/_Game/Prefabs/Characters",
    "Assets/_Game/Prefabs/Environment",
    "Assets/_Game/Materials",
    "Assets/_Game/Textures",
    "Assets/_Game/Audio/BGM",
    "Assets/_Game/Audio/SFX",
    "Assets/_Game/Scenes",
    "Assets/_Game/Settings"
]

class UnityGameArchitect:
    @staticmethod
    def initialize_project(project_name: str, target_root: str = "") -> Path:
        base_dir = Path(target_root) if target_root else workspace.get_desktop_dir() / project_name
        print(f"\n[*] Ultron Architecting Enterprise Game Pipeline: {project_name}")

        # 1. Folder structure deployment
        for folder_path in COMMERCIAL_PROJECT_LAYOUT:
            (base_dir / folder_path).mkdir(parents=True, exist_ok=True)

        # 2. Deploy core C# foundation scripts via streaming writer
        core_dir = base_dir / "Assets/_Game/Scripts/Core"
        player_dir = base_dir / "Assets/_Game/Scripts/Player"

        stream_writer.stream_to_file(core_dir / "GameManager.cs", templates.GAME_MANAGER_CS)
        stream_writer.stream_to_file(player_dir / "PlayerController.cs", templates.PLAYER_CONTROLLER_CS)

        print(f"[Ultron]: Game architecture initialized at '{base_dir}'. Standardized directory structure locked.")
        return base_dir

game_architect = UnityGameArchitect()
