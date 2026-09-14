"""
Universal Studio Interactive Loop.
Adapts dynamically to any genre, coordinates LLM generation, and avoids manual copy-pasting.
"""
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skills.game_engine_architect.interview_cortex import conduct_director_interview
from skills.game_engine_architect.universal_pipeline import generate_native_terrain_architect_csharp
from skills.game_engine_architect.hub_registry import register_project_in_hub
from skills.game_engine_architect.project_manifest import inject_project_manifest
from skills.game_engine_architect.dispatcher import dispatcher

def launch_universal_studio():
    # 1. Run Dynamic Discovery Interview
    bible = conduct_director_interview()

    # 2. Setup Project Folder
    proj_dir = Path.home() / "UnityProjects" / bible.title
    proj_dir.mkdir(parents=True, exist_ok=True)
    inject_project_manifest(proj_dir)
    register_project_in_hub(proj_dir)

    # Open Explorer window
    os.startfile(str(proj_dir))

    # 3. Inject Universal World Architect C# Script
    editor_dir = proj_dir / "Assets" / "_Game" / "Editor"
    editor_dir.mkdir(parents=True, exist_ok=True)
    
    terrain_csharp = generate_native_terrain_architect_csharp(bible)
    (editor_dir / "WorldArchitectGenerator.cs").write_text(terrain_csharp, encoding="utf-8")
    print(f"\n[ULTRON]: Injected WorldArchitectGenerator.cs into project.")

    # 4. LLM Generation for Custom Mechanics
    print("\n[ULTRON_DEV]: Analyzing mechanics & generating custom gameplay logic via LM Studio...")
    system_role = (
        "You are ULTRON, a AAA Unity 6 C# Lead Architect. "
        "Write clean, complete C# MonoBehaviour scripts. "
        "Ensure no syntax errors and using UnityEngine directives are present."
    )
    prompt = (
        f"Generate a C# system named 'GameDirector_{bible.title}' for Unity 6. "
        f"Genre: {bible.genre}. Art Style: {bible.art_style}. Perspective: {bible.perspective}. "
        f"Mechanics to initialize: {', '.join(bible.core_mechanics)}. "
        f"Story hook: {bible.narrative_hook}. Implement clean modular code."
    )
    raw_code = dispatcher.ask(system_role, prompt, max_tokens=2200)
    if raw_code:
        code = dispatcher.extract_code(raw_code, "csharp")
        scripts_dir = proj_dir / "Assets" / "_Game" / "Scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        (scripts_dir / f"GameDirector_{bible.title}.cs").write_text(code, encoding="utf-8")
        print(f"[ULTRON_DEV]: Gameplay manager 'GameDirector_{bible.title}.cs' generated & deployed!")

    print("\n" + "="*70)
    print(f"   [SUCCESS] '{bible.title}' initialized with Universal Architecture!")
    print(f"   1. Unity Hub kholo -> '{bible.title}' open karo.")
    print("   2. Top menu se click karo: Ultron -> 1. Generate Native World Environment.")
    print("="*70)

if __name__ == "__main__":
    launch_universal_studio()
