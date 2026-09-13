"""
Ultron Multi-Agent Studio Runtime with Memory Persistence & Task Tracking.
"""
from __future__ import annotations
import sys
import time
import subprocess
from pathlib import Path
from importlib import import_module

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

workspace = import_module("skills.workspace_tools").workspace
banter = import_module("skills.banter_engine").banter_engine
detector = import_module("skills.game_engine_architect.unity_detector")
manifest = import_module("skills.game_engine_architect.project_manifest")

# Memory linkages
try:
    memory_cortex = import_module("01_Memory.memory_cortex").memory_cortex
    pending_actions = import_module("01_Memory.pending_actions").pending_actions
except Exception as e:
    print(f"[WARN] Memory linkage offline: {e}")
    memory_cortex = None
    pending_actions = None

from skills.game_engine_architect.agents import atlas, archon, ultron_dev, aura, cipher
from skills.game_engine_architect.engines import world_engine, actor_engine, systems_engine, ai_engine, render_engine

class StudioRuntime:
    @staticmethod
    def speak(speaker: str, text: str):
        formatted = f"[{speaker}]: {text}"
        print(f"\n{formatted}")
        banter._speak_safe(f"{speaker} bol raha hai: {text}")

    @staticmethod
    def start_session():
        unity_exe = detector.get_unity_binary()
        if not unity_exe:
            StudioRuntime.speak("ULTRON", "Unity 6 engine binary detect nahi hua. Unity Hub verify kar.")
            return

        print("\n" + "="*70)
        print("   >>> ULTRON MULTI-AGENT AAA PRODUCTION STUDIO ACTIVE <<<   ")
        print("="*70)

        title = input("\n[Project Setup] Game Title: ").strip() or "Project_Titan"
        genre = input("[Project Setup] Genre (FPS / Survival / RPG / Roguelike): ").strip() or "Survival"
        vision = input("[Project Setup] High Concept Vision: ").strip() or "Gritty atmospheric survival against mutant hordes"

        desktop = workspace.get_desktop_dir()
        proj_dir = desktop / title
        proj_dir.mkdir(parents=True, exist_ok=True)
        manifest.inject_project_manifest(proj_dir)

        # Sync project metadata into Memory
        if pending_actions:
            pending_actions.set_active_project(title, {"genre": genre, "vision": vision, "path": str(proj_dir)})
        if memory_cortex:
            memory_cortex.consolidate_turn_to_ltm("active_game", f"{title} | {genre} | {vision}", "project_meta")

        # Launch Unity 6 in background
        subprocess.Popen(f'"{unity_exe}" -projectPath "{proj_dir}"', shell=True)

        # --- MILESTONE 1: ATLAS ROADMAP ---
        task_id = "milestone_1_roadmap"
        if pending_actions: pending_actions.register_task(task_id, "ATLAS", "Plan Master Roadmap")
        StudioRuntime.speak("ATLAS", f"Roadmap lock kar raha hoon for {title}...")
        plan = atlas.plan_project(genre, vision)
        print(f"\n--- [ATLAS MASTER ROADMAP] ---\n{plan}\n------------------------------")
        if pending_actions: pending_actions.update_task_status(task_id, "completed")
        if memory_cortex: memory_cortex.ltm.log_episode("milestone", f"Roadmap locked for {title}")
        time.sleep(1.5)

        # --- MILESTONE 2: WORLD ASSEMBLY ---
        task_id = "milestone_2_world"
        if pending_actions: pending_actions.register_task(task_id, "ULTRON", "Generate Procedural Terrain")
        StudioRuntime.speak("ARCHON", "Project directory structure aur URP packages bind ho gaye.")
        StudioRuntime.speak("AURA", "Biome visual parameters evaluate kar rahi hoon.")
        biome_desc = input("\n[Director Input] Biome & Terrain Description: ").strip() or "Dense pine forest with granite ridges"
        world_script = world_engine.build_terrain_generator(proj_dir, biome_desc)
        StudioRuntime.speak("ULTRON", f"Terrain builder C# inject ho gaya: {world_script.name}.")
        if pending_actions: pending_actions.update_task_status(task_id, "completed")
        if memory_cortex: memory_cortex.ltm.log_episode("milestone", f"Terrain generated with biome: {biome_desc}")
        time.sleep(1.5)

        # --- MILESTONE 3: ACTOR & CAMERA ---
        task_id = "milestone_3_actor"
        if pending_actions: pending_actions.register_task(task_id, "ULTRON", "Build Player Controller")
        control_style = input("\n[Director Input] Player Movement Style: ").strip() or "First-Person Survival"
        actor_script = actor_engine.build_player_controller(proj_dir, control_style)
        StudioRuntime.speak("CIPHER", f"Movement kinetics checked. Script: {actor_script.name}.")
        if pending_actions: pending_actions.update_task_status(task_id, "completed")
        time.sleep(1.5)

        # --- MILESTONE 4: SYSTEMS & AI ---
        task_id = "milestone_4_ai"
        if pending_actions: pending_actions.register_task(task_id, "ULTRON", "Build AI Threat Brain")
        threat = input("\n[Director Input] Main Threat/Enemy Type: ").strip() or "Nocturnal Mutant"
        ai_script = ai_engine.build_enemy_agent(proj_dir, threat)
        StudioRuntime.speak("ULTRON", f"AI Brain with FSM logic deployed: {ai_script.name}.")
        if pending_actions: pending_actions.update_task_status(task_id, "completed")

        StudioRuntime.speak("ATLAS", "Milestones completed! Unity Editor window me scene verify karo.")

studio_runtime = StudioRuntime()
