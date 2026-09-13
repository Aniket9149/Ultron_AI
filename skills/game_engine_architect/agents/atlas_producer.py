from skills.game_engine_architect.dispatcher import dispatcher

class AtlasProducer:
    ROLE = (
        "You are ATLAS, an elite AAA Game Executive Producer. You define strict, "
        "step-by-step production roadmaps without scope creep. Keep milestones razor-sharp."
    )

    @staticmethod
    def plan_project(genre: str, vision: str) -> str:
        prompt = f"Create a strict 5-stage milestone roadmap for a commercial PC game.\nGenre: {genre}\nVision: {vision}"
        return dispatcher.ask(AtlasProducer.ROLE, prompt, max_tokens=800)

atlas = AtlasProducer()
