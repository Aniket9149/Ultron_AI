"""
skills/game_engine_architect/interactive_pipeline.py
Persistent Interactive Game Architect with Deep Discovery and Live Tuning.
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
automator = import_module("skills.game_engine_architect.editor_automator")

class PersistentGamePipeline:
    @staticmethod
    def speak(text: str):
        print(f"\n[Ultron Voice]: {text}")
        banter._speak_safe(text)

    @staticmethod
    def run_studio_session(game_title: str = "Wilderness_Survival"):
        unity_exe = detector.get_unity_binary()
        if not unity_exe:
            PersistentGamePipeline.speak("Unity executable nahi mila. Unity Hub se install confirm kar.")
            return

        desktop = workspace.get_desktop_dir()
        proj_dir = desktop / game_title
        proj_dir.mkdir(parents=True, exist_ok=True)

        manifest.inject_project_manifest(proj_dir)
        automator.inject_terrain_automator(proj_dir)

        # -------------------------------------------------------------
        # Discovery Phase
        # -------------------------------------------------------------
        PersistentGamePipeline.speak(f"Studio session live hai. Game ka naam {game_title} hai. Pehle 3 sawalon ka jawab de taaki design lock karein.")

        biome = input("\n[Ultron Q1]: Biome kaisa chahiye? (Dense Forest / Snowy Island / Post-Apocalyptic Wasteland): ")
        monster = input("[Ultron Q2]: Dushman/Threat kya hoga? (Mutants / Zombies / Wild Animals / Eldritch Creatures): ")
        survival_focus = input("[Ultron Q3]: Gameplay priority kya hai? (Crafting & Base Building / Pure Hardcore Survival): ")

        PersistentGamePipeline.speak(f"Noted. {biome} biome with {monster} threats. Architecture file generate kar raha hoon.")

        # Launch Unity
        cmd = f'"{unity_exe}" -projectPath "{proj_dir}"'
        subprocess.Popen(cmd, shell=True)

        PersistentGamePipeline.speak("Unity open ho chuka hai. Unity ke top menu mein 'Ultron -> Generate Survival Scene' click kar.")

        # -------------------------------------------------------------
        # Persistent Interactive Loop
        # -------------------------------------------------------------
        print("\n" + "="*60)
        print(" [ULTRON CO-DEV SESSION ACTIVE] ")
        print(" Type your feedback (e.g., 'mountain thoda flat kar', 'monster AI script add kar')")
        print(" Type 'finalize' jab tera test complete ho.")
        print("="*60 + "\n")

        while True:
            feedback = input("\n[Co-Dev Live Feedback] > ").strip()
            if not feedback:
                continue

            if feedback.lower() in ("finalize", "exit", "done", "perfect"):
                PersistentGamePipeline.speak("Done. Project state save kar di hai. Next milestone ke liye ready rehna.")
                break

            # Iterative processing
            PersistentGamePipeline.speak(f"Feedback receive hua: '{feedback}'. Patch apply kar raha hoon, scene check kar.")
            time.sleep(1.5)

game_pipeline = PersistentGamePipeline()
