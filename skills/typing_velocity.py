"""
skills/typing_velocity.py
Dynamic typing speed controller for Ultron.
Calculates typing velocity curves based on payload line volume.
"""

def calculate_velocity_profile(total_lines: int) -> dict:
    if total_lines <= 50:
        return {
            "mode": "human_char",
            "char_delay": (0.012, 0.035),
            "line_delay": 0.08
        }
    elif total_lines <= 200:
        return {
            "mode": "fast_char",
            "char_delay": (0.002, 0.005),
            "line_delay": 0.015
        }
    else:
        # Massive codebase (500+ lines): burst lines with minimal delay
        dynamic_line_delay = max(0.0005, 1.5 / total_lines)
        return {
            "mode": "line_stream",
            "line_delay": dynamic_line_delay
        }
