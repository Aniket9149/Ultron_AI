"""
skills/stream_writer.py
Non-blocking streaming file writer.
Simulates active real-time typing directly into target workspace files.
"""
import time
import random
from pathlib import Path
from skills.typing_velocity import calculate_velocity_profile

class CodeStreamWriter:
    @staticmethod
    def stream_to_file(file_path: Path, code_content: str) -> None:
        lines = code_content.splitlines(keepends=True)
        total_lines = len(lines)
        profile = calculate_velocity_profile(total_lines)
        mode = profile["mode"]

        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

        if mode in ("human_char", "fast_char"):
            min_d, max_d = profile["char_delay"]
            line_d = profile["line_delay"]

            with open(file_path, "a", encoding="utf-8", buffering=1) as f:
                for line in lines:
                    for char in line:
                        f.write(char)
                        f.flush()
                        time.sleep(random.uniform(min_d, max_d))
                    time.sleep(line_d)
        else:
            line_d = profile["line_delay"]
            with open(file_path, "a", encoding="utf-8", buffering=1) as f:
                for line in lines:
                    f.write(line)
                    f.flush()
                    if line_d > 0:
                        time.sleep(line_d)

stream_writer = CodeStreamWriter()
