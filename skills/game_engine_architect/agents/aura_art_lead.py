from skills.game_engine_architect.dispatcher import dispatcher

class AuraArtLead:
    ROLE = (
        "You are AURA, Technical Art and Visual Realism Director. "
        "You enforce PBR material standards, realistic lighting color temperatures, URP volumes, "
        "volumetric fog density, and 1:1 real-world metric scales."
    )

    @staticmethod
    def audit_visuals(biome: str, mood: str) -> str:
        prompt = f"Define exact PBR material channels, URP lighting parameters, and fog density for:\nBiome: {biome}\nAtmosphere: {mood}"
        return dispatcher.ask(AuraArtLead.ROLE, prompt, max_tokens=700)

aura = AuraArtLead()
