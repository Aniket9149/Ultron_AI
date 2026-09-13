from pathlib import Path
from skills.game_engine_architect.agents.ultron_core import ultron_dev

class SystemsEngine:
    @staticmethod
    def build_core_system(project_dir: Path, system_type: str) -> Path:
        target = project_dir / "Assets" / "_Game" / "Scripts" / "Core" / f"{system_type}Manager.cs"
        target.parent.mkdir(parents=True, exist_ok=True)
        spec = f"Production Unity 6 Singleton Manager handling {system_type} with events and save state hooks."
        ultron_dev.write_script(target, spec)
        return target

systems_engine = SystemsEngine()
