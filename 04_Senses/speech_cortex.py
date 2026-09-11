"""
04_Senses/speech_cortex.py
Upgraded Speech Cortex using 'base' model with vocabulary biasing.
"""
from __future__ import annotations
import tempfile
from pathlib import Path
from faster_whisper import WhisperModel

class SpeechCortex:
    def __init__(self, model_size: str = "base") -> None:
        print("[*] Initializing Speech Cortex (base engine)...")
        # 'base' strikes the ideal balance between speed and Indian accent accuracy
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        # Vocabulary guidance for phonetic anchoring
        self.prompt_bias = "Ultron, Aniket, Jarvis, system status, execute, terminal, code, override."

    def transcribe(self, wav_bytes: bytes) -> str:
        if not wav_bytes:
            return ""

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            f.write(wav_bytes)

        try:
            segments, _ = self.model.transcribe(
                temp_path,
                beam_size=3,
                initial_prompt=self.prompt_bias,
                vad_filter=True
            )
            text = " ".join([seg.text.strip() for seg in segments]).strip()
            return text
        except Exception as exc:
            print(f"[SPEECH_CORTEX_ERROR]: {exc}")
            return ""
        finally:
            Path(temp_path).unlink(missing_ok=True)

speech_cortex = SpeechCortex()
