"""
Universal Game Director Interview Cortex.
Extracts deep design specs for ANY game genre, art style, and mechanical depth.
"""
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class GameDesignBible:
    title: str = "Untitled_Project"
    genre: str = "Action"
    art_style: str = "Semi-Realistic"
    perspective: str = "Third-Person"
    world_scale: str = "Medium (500x500m)"
    topography: str = "Rugged Mountains with Valleys"
    core_mechanics: List[str] = field(default_factory=list)
    threats_ecosystem: str = "Dynamic Reactive AI"
    atmosphere_lighting: str = "Volumetric Fog & Dynamic Day/Night"
    narrative_hook: str = ""

def conduct_director_interview() -> GameDesignBible:
    bible = GameDesignBible()
    print("\n" + "="*70)
    print("   >>> ULTRON UNIVERSAL GAME ENGINE ARCHITECT <<<")
    print("   [Phase 1: Creative & Technical Discovery Pipeline]")
    print("="*70)

    bible.title = input("\n[1/7] Project Title (e.g. Mythic_Isle / Neon_Racer / Cyber_Siege): ").strip() or "Universal_Masterpiece"
    
    print("\n[2/7] Core Genre & Sub-Genre Archetype:")
    print("  1. Survival Exploration (Resource loops, shelter crafting, elemental powers)")
    print("  2. Atmospheric Action RPG (Combat combos, leveling, questing, shrines)")
    print("  3. High-Speed Physics / Racing / Sim")
    print("  4. Sci-Fi Roguelite / Shooter (Procedural dungeons, weapon synergies)")
    print("  5. Custom / Experimental")
    g_choice = input("Select (1-5) or type custom: ").strip()
    g_map = {"1": "Survival Exploration", "2": "Atmospheric Action RPG", "3": "Physics Sim / Racing", "4": "Sci-Fi Roguelite", "5": "Experimental"}
    bible.genre = g_map.get(g_choice, g_choice or "Survival Exploration")

    print("\n[3/7] Visual Fidelity & Art Direction:")
    print("  1. Ghost of Tsushima Aesthetic (Wind-swept grass, volumetric mist, rich color grading)")
    print("  2. Hyper-Realistic Gritty (Wet mud, dark shadows, high-contrast HDRP/URP)")
    print("  3. Stylized Low-Poly / Painterly (Zelda / Valheim inspired)")
    print("  4. Dark Fantasy Gothic (Elden Ring desaturated stone, eerie glow)")
    v_choice = input("Select (1-4) or type custom: ").strip()
    v_map = {"1": "Ghost of Tsushima Wind-Swept Style", "2": "Photorealistic Gritty", "3": "Stylized Painterly", "4": "Dark Fantasy Gothic"}
    bible.art_style = v_map.get(v_choice, v_choice or "Ghost of Tsushima Wind-Swept Style")

    print("\n[4/7] Camera & Control Perspective:")
    print("  1. Third-Person Over-the-Shoulder (Cinematic movement & melee/magic focus)")
    print("  2. Immersive First-Person (Survival body presence, tool handling)")
    print("  3. Top-Down / Isometric Tactical")
    c_choice = input("Select (1-3) or type custom: ").strip()
    c_map = {"1": "Third-Person Cinematic", "2": "First-Person Immersive", "3": "Top-Down Tactical"}
    bible.perspective = c_map.get(c_choice, c_choice or "Third-Person Cinematic")

    print("\n[5/7] World Topography & Geography:")
    print("  1. Rugged Island (Shipwreck coastline, inland pine valleys, jagged mountain peaks)")
    print("  2. Continental Forest & River Basin (Rolling hills, dense trees, waterfall streams)")
    print("  3. Desert Canyon / Wasteland (Plateaus, sandy dunes, rocky gorges)")
    print("  4. Enclosed Dungeon / Modular Arena")
    w_choice = input("Select (1-4) or type custom: ").strip()
    w_map = {"1": "Rugged Island with Coastlines & Peaks", "2": "Continental Forest & River Basin", "3": "Desert Canyon Wasteland", "4": "Enclosed Modular Arena"}
    bible.topography = w_map.get(w_choice, w_choice or "Rugged Island with Coastlines & Peaks")

    bible.narrative_hook = input("\n[6/7] Narrative Hook & Lore (Story summary, motivations, origin): ").strip()
    
    print("\n[7/7] Core Gameplay Mechanics (Enter comma-separated features):")
    print("  Example: Elemental Magic (Fire/Forest/Earth), Sound-based mutant stealth, NPC Colony, Farming")
    m_input = input("Features: ").strip()
    bible.core_mechanics = [m.strip() for m in m_input.split(",") if m.strip()] if m_input else ["Resource Gathering", "Survival Vitals", "Elemental Magic", "Sound Stealth"]

    return bible
