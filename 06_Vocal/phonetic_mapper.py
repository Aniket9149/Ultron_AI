"""Tight phonetic mapping for smooth neural vocal output."""

from __future__ import annotations

import re


LATIN_TECH_KEYWORDS = {
    "ultron", "browser", "brave", "chrome", "youtube", "shorts", "video",
    "click", "scroll", "tab", "window", "screen", "active", "online",
    "pointer", "cursor", "system", "command", "task", "link", "google", "enter",
}

CORE_VOCAB_MAP = {
    "aniket": "अनिकेत", "main": "मैं", "mujhe": "मुझे", "mera": "मेरा", "meri": "मेरी", "mere": "मेरे",
    "tum": "तुम", "tumhe": "तुम्हें", "tumhara": "तुम्हारा", "aap": "आप", "aapka": "आपका",
    "hai": "है", "hain": "हैं", "hoon": "हूँ", "ho": "हो", "tha": "था", "thi": "थी", "the": "थे",
    "par": "पर", "per": "पर", "pe": "पे", "se": "से", "ko": "को", "ka": "का", "ki": "की", "ke": "के",
    "me": "में", "mein": "में", "aur": "और", "ya": "या", "bhi": "भी", "toh": "तो", "to": "तो",
    "na": "ना", "mat": "मत", "nahi": "नहीं", "nhi": "नहीं", "kuch": "कुछ", "sirf": "सिर्फ",
    "kar": "कर", "karo": "करो", "karna": "करना", "karein": "करें",
    "chal": "चल", "chalo": "चलो", "chalao": "चलाओ", "dekh": "देख", "dekho": "देखो",
    "bol": "बोल", "bolo": "बोलो", "rok": "रोक", "roko": "रोको", "aao": "आओ", "jao": "जाओ",
    "kya": "क्या", "kyun": "क्यों", "kaise": "कैसे", "kahan": "कहाँ", "kab": "कब",
    "bas": "बस", "abhi": "अभी", "thoda": "थोड़ा", "ek": "एक", "do": "दो",
    "samne": "सामने", "dhyan": "ध्यान", "kaam": "काम", "scene": "सीन",
}


class PhoneticMapper:
    """Convert known Roman Hinglish words without damaging tech terms."""

    def map_for_neural_tts(self, text: str) -> str:
        if not text:
            return ""

        clean_text = re.sub(r"[.\-_,]{2,}", " ", text)
        clean_text = re.sub(r"[_*#@$^~]", "", clean_text)
        words = re.findall(r"[\w']+|[.,!?]", clean_text)
        result = []

        for token in words:
            low = token.casefold()
            if low in LATIN_TECH_KEYWORDS:
                result.append(token)
            elif low in CORE_VOCAB_MAP:
                result.append(CORE_VOCAB_MAP[low])
            else:
                result.append(token)

        output = " ".join(result)
        output = re.sub(r"\s+([.,!?])", r"\1", output)
        return re.sub(r"\s+", " ", output).strip()


phonetic_mapper = PhoneticMapper()