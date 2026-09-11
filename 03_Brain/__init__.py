import sys
from pathlib import Path

# Alias 03_Brain as brain globally so legacy imports work without duplicate folders
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.modules["brain"] = sys.modules[__name__]
