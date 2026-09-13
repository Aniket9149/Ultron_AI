from skills.game_engine_architect.dispatcher import dispatcher

class ArchonArchitect:
    ROLE = (
        "You are ARCHON, Lead Technical Systems Architect for Unity 6. "
        "You design robust C# namespaces, ScriptableObject architectures, and clean folder structures."
    )

    @staticmethod
    def design_architecture(genre: str, mechanics: str) -> str:
        prompt = f"Design the C# architecture contracts and required components for:\nGenre: {genre}\nMechanics: {mechanics}"
        return dispatcher.ask(ArchonArchitect.ROLE, prompt, max_tokens=900)

archon = ArchonArchitect()
