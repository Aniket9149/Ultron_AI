from pathlib import Path
from skills.game_engine_architect.agents.ultron_core import ultron_dev

class AIEngine:
    @staticmethod
    def build_enemy_agent(project_dir: Path, enemy_type: str) -> Path:
        target = project_dir / "Assets" / "_Game" / "Scripts" / "AI" / f"{enemy_type}Brain.cs"
        target.parent.mkdir(parents=True, exist_ok=True)
        spec = (
            f"NavMeshAgent-based FSM enemy brain for '{enemy_type}'. "
            "States: Patrol, Search, Chase, Attack. Includes vision raycast and sound detection."
        )
        ultron_dev.write_script(target, spec)
        return target

ai_engine = AIEngine()
