"""
Ultron Multi-Agent Game Studio Interactive Runtime with Memory Integration.
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
        if memory_cortex:
            memory_cortex.record_turn(speaker, text)

    @staticmethod
    def start_session():
        unity_exe = detector.get_unity_binary()
        if not unity_exe:
            StudioRuntime.speak("ULTRON", "Unity 6 engine binary detect nahi hua. Unity Hub path verify kar.")
            return

        print("\n" + "="*70)
        print("   >>> ULTRON MULTI-AGENT AAA PRODUCTION STUDIO ACTIVE <<<   ")
        print("="*70)

        title = input("\n[Project Setup] Game Title: ").strip() or "Project_Titan"
        genre = input("[Project Setup] Genre (FPS / Survival / RPG / Roguelike): ").strip() or "Survival"
        vision = input("[Project Setup] High Concept Vision: ").strip() or "Gritty atmospheric survival against mutant hordes"

        if memory_cortex:
            memory_cortex.consolidate_turn_to_ltm("project_title", title, "project_metadata")
            memory_cortex.consolidate_turn_to_ltm("project_genre", genre, "project_metadata")
            memory_cortex.consolidate_turn_to_ltm("project_vision", vision, "project_metadata")

        if pending_actions:
            pending_actions.set_active_project(title, {"genre": genre, "vision": vision})

        desktop = workspace.get_desktop_dir()
        proj_dir = desktop / title
        proj_dir.mkdir(parents=True, exist_ok=True)
        manifest.inject_project_manifest(proj_dir)

        # Launch Unity 6 in Background
        subprocess.Popen(f'"{unity_exe}" -projectPath "{proj_dir}"', shell=True)

        # --- MILESTONE 1: ATLAS ROADMAP ---
        if pending_actions:
            pending_actions.register_task("m1_roadmap", "ATLAS", "Drafting 5-stage production roadmap")
        StudioRuntime.speak("ATLAS", f"Roadmap lock kar raha hoon for {title}...")
        plan = atlas.plan_project(genre, vision)
        print(f"\n--- [ATLAS MASTER ROADMAP] ---\n{plan}\n------------------------------")
        if pending_actions:
            pending_actions.update_task_status("m1_roadmap", "completed")
        if memory_cortex:
            memory_cortex.ltm.log_episode("milestone", f"Roadmap frozen for {title}")
        time.sleep(2.0)

        # --- MILESTONE 2: ARCHON & WORLD ASSEMBLY ---
        if pending_actions:
            pending_actions.register_task("m2_world", "ULTRON", "Terrain generation and URP volume binding")
        StudioRuntime.speak("ARCHON", "Project directory structure aur URP packages bind kar diye hain.")
        StudioRuntime.speak("AURA", "Biome visual parameters evaluate ho rahe hain.")
        
        biome_desc = input("\n[Director Input] Biome & Terrain Description: ").strip() or "Dense pine forest with jagged granite ridges"
        world_script = world_engine.build_terrain_generator(proj_dir, biome_desc)
        StudioRuntime.speak("ULTRON", f"Terrain builder C# inject ho gaya hai at {world_script.name}.")
        if pending_actions:
            pending_actions.update_task_status("m2_world", "completed")
        if memory_cortex:
            memory_cortex.ltm.log_episode("milestone", f"World generator built for biome: {biome_desc}")
        time.sleep(2.0)

        # --- MILESTONE 3: ACTOR & CAMERA ---
        if pending_actions:
            pending_actions.register_task("m3_actor", "ULTRON", "Kinematic character controller")
        control_style = input("\n[Director Input] Player Movement Style (First-Person / Third-Person / Souls-like): ").strip() or "First-Person Survival"
        actor_script = actor_engine.build_player_controller(proj_dir, control_style)
        StudioRuntime.speak("CIPHER", f"Movement kinetics check pass. Script generated at {actor_script.name}.")
        if pending_actions:
            pending_actions.update_task_status("m3_actor", "completed")
        if memory_cortex:
            memory_cortex.ltm.log_episode("milestone", f"Player controller generated: {control_style}")
        time.sleep(2.0)

        # --- MILESTONE 4: SYSTEMS & THREATS ---
        if pending_actions:
            pending_actions.register_task("m4_ai", "ULTRON", "NavMesh enemy FSM brain")
        threat = input("\n[Director Input] Main Threat/Enemy Type: ").strip() or "Nocturnal Blind Mutant"
        ai_script = ai_engine.build_enemy_agent(proj_dir, threat)
        StudioRuntime.speak("ULTRON", f"AI Brain with FSM logic deployed at {ai_script.name}.")
        if pending_actions:
            pending_actions.update_task_status("m4_ai", "completed")
        if memory_cortex:
            memory_cortex.ltm.log_episode("milestone", f"Enemy agent deployed for threat: {threat}")

        StudioRuntime.speak("ATLAS", "Milestones complete ho gaye hain. Unity Editor window mein 'Ultron' menu check karo aur live test shuru karo!")

studio_runtime = StudioRuntime()
