# -*- coding: utf-8 -*-
"""
ULTRON WAKE WORD DETECTOR (01_Voice)
"""
import speech_recognition as sr

class UltronWakeDetector:
    def __init__(self):
        self.triggers = ["ultron", "ultrone", "hey ultron", "altron", "oltron"]
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 280
        self.recognizer.dynamic_energy_threshold = True

    def listen_for_wake_word(self, source) -> bool:
        try:
            audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=3.0)
            text = self.recognizer.recognize_google(audio, language="en-IN").lower().strip()
            print(f"[AMBIENT MIC]: \"{text}\"")
            for trigger in self.triggers:
                if trigger in text:
                    return True
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except Exception:
            pass
        return False

wake_detector = UltronWakeDetector()
