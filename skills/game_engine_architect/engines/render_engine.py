from pathlib import Path
from skills.game_engine_architect.agents.ultron_core import ultron_dev

class RenderEngine:
    @staticmethod
    def build_atmosphere_setup(project_dir: Path, atmosphere_spec: str) -> Path:
        target = project_dir / "Assets" / "Editor" / "AtmosphereSetup.cs"
        target.parent.mkdir(parents=True, exist_ok=True)
        spec = (
            f"Unity Editor script to configure URP Global Volume, directional sun angle, "
            f"color grading, and volumetric fog matching: {atmosphere_spec}."
        )
        ultron_dev.write_script(target, spec)
        return target

render_engine = RenderEngine()
