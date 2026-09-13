from pathlib import Path
from skills.game_engine_architect.agents.ultron_core import ultron_dev

class ActorEngine:
    @staticmethod
    def build_player_controller(project_dir: Path, control_style: str) -> Path:
        target = project_dir / "Assets" / "_Game" / "Scripts" / "Player" / "PlayerEntityController.cs"
        target.parent.mkdir(parents=True, exist_ok=True)
        spec = (
            f"CharacterController-based modular player controller for Unity 6 with style: {control_style}. "
            "Includes smooth movement, sprint, jump physics, and camera rotation hooks."
        )
        ultron_dev.write_script(target, spec)
        return target

actor_engine = ActorEngine()
