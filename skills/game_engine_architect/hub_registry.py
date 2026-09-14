"""
Official Unity Hub CLI Project Registrar.
"""
import subprocess
from pathlib import Path

HUB_EXE = Path(r"C:\Program Files\Unity Hub\Unity Hub.exe")

def register_project_in_hub(project_path: Path):
    if not HUB_EXE.exists():
        return
    try:
        cmd = [str(HUB_EXE), "--", "--headless", "project-add", str(project_path.resolve())]
        subprocess.run(cmd, capture_output=True, timeout=10)
        print(f"[UNITY_HUB]: '{project_path.name}' officially registered in Unity Hub.")
    except Exception as e:
        print(f"[UNITY_HUB_WARN]: CLI register failed: {e}")
