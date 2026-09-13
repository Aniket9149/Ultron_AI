from pathlib import Path
from skills.game_engine_architect.agents.ultron_core import ultron_dev

class WorldEngine:
    @staticmethod
    def build_terrain_generator(project_dir: Path, biome_spec: str) -> Path:
        target = project_dir / "Assets" / "Editor" / "ProceduralWorldBuilder.cs"
        target.parent.mkdir(parents=True, exist_ok=True)
        spec = (
            f"An Editor script with [MenuItem('Ultron/Generate World')] creating procedural Unity Terrain "
            f"with Perlin Noise heights matching biome: {biome_spec}."
        )
        ultron_dev.write_script(target, spec)
        return target

world_engine = WorldEngine()
