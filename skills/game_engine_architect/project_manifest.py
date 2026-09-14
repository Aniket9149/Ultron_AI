"""
Project Manifest and Metadata Generator for Unity 6.
Prevents "Open or Create New" popups by seeding valid Unity project structure.
"""
from pathlib import Path

def inject_project_manifest(proj_dir: Path):
    settings_dir = proj_dir / "ProjectSettings"
    settings_dir.mkdir(parents=True, exist_ok=True)

    # Inject ProjectVersion to satisfy Unity CLI launcher
    version_file = settings_dir / "ProjectVersion.txt"
    if not version_file.exists():
        version_file.write_text("m_EditorVersion: 6000.5.5f1\nm_EditorVersionWithRevision: 6000.5.5f1 (custom)\n", encoding="utf-8")

    # Ensure Assets and Packages folders exist
    (proj_dir / "Assets").mkdir(parents=True, exist_ok=True)
    (proj_dir / "Packages").mkdir(parents=True, exist_ok=True)

    manifest_file = proj_dir / "Packages" / "manifest.json"
    if not manifest_file.exists():
        manifest_file.write_text(
            '{\n  "dependencies": {\n    "com.unity.render-pipelines.universal": "17.0.3",\n    "com.unity.inputsystem": "1.7.0"\n  }\n}',
            encoding="utf-8"
        )
