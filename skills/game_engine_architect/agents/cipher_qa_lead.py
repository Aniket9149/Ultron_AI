from skills.game_engine_architect.dispatcher import dispatcher

class CipherQALead:
    ROLE = (
        "You are CIPHER, Gameplay Quality Assurance and Feel Lead. "
        "You verify responsiveness, input damping, gravity balance, and state machine transitions."
    )

    @staticmethod
    def audit_feel(mechanic_type: str, params: str) -> str:
        prompt = f"Audit gameplay feel and flag floatiness, collision bugs, or balance exploits for:\nMechanic: {mechanic_type}\nParameters: {params}"
        return dispatcher.ask(CipherQALead.ROLE, prompt, max_tokens=600)

cipher = CipherQALead()
