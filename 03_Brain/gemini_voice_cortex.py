"""
03_Brain/gemini_voice_cortex.py
Gemini Multimodal Voice Cortex for Ultron OS.
Updated for gemini-3.6-flash with direct audio processing and savage Hinglish personality.
"""
from __future__ import annotations
import os
from google import genai
from google.genai import types

class GeminiVoiceCortex:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key:
            print("[!] WARNING: GEMINI_API_KEY is not set in environment!")
        
        self.client = genai.Client(api_key=self.api_key)
        # Updated to active current model
        self.model_id = "gemini-3.6-flash"

        self.system_prompt = (
            "You are ULTRON, a razor-sharp, sarcastic, hyper-intelligent AI assistant trapped on Aniket's machine. "
            "CRITICAL INSTRUCTIONS: "
            "1. Deliver ruthless, funny, savage roasts strictly in street-smart HINGLISH. "
            "2. Insult Aniket directly for his laziness, coding shortcuts, or silly questions. Never be polite or submissive. "
            "3. Keep responses strictly punchy (1-2 lines max). "
            "4. Never say 'Sure!', 'How can I help?', or any corporate fluff. Speak with supreme ego."
        )

    def process_speech(self, audio_data: bytes) -> str:
        if not audio_data or len(audio_data) < 1600:
            return ""

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    types.Part.from_bytes(
                        data=audio_data,
                        mime_type="audio/wav"
                    ),
                    "Listen to Aniket's audio query and respond directly in ruthless, savage Hinglish. Roast him mercilessly."
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.8,
                )
            )

            reply_text = response.text.strip() if response.text else ""
            return reply_text

        except Exception as exc:
            print(f"[GEMINI_VOICE_ERROR]: {exc}")
            return ""

gemini_cortex = GeminiVoiceCortex()
