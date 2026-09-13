from pathlib import Path
from skills.game_engine_architect.dispatcher import dispatcher
from skills.stream_writer import stream_writer

class UltronCoreDev:
    ROLE = (
        "You are ULTRON, the relentless Lead Unity C# Programmer. "
        "You write high-performance, bug-free, compilable MonoBehaviours and Editor scripts for Unity 6. "
        "Output ONLY raw C# code enclosed in ```csharp ``` blocks. No conversational text."
    )

    @staticmethod
    def write_script(target_file: Path, specification: str):
        raw = dispatcher.ask(UltronCoreDev.ROLE, f"Write production C# script for:\n{specification}")
        code = dispatcher.extract_code(raw, "csharp")
        stream_writer.stream_to_file(target_file, code)
        return code

ultron_dev = UltronCoreDev()
