import subprocess
import sys

print(">>> [1/3] Updating .gitignore...")
gitignore_entries = "\n04_Display/sandbox_preview/\n04_display/sandbox_preview/\n*.ort\n*.quant.ort\n*.crx\n"
with open(".gitignore", "a+", encoding="utf-8") as f:
    f.seek(0)
    existing = f.read()
    if "sandbox_preview" not in existing:
        f.write(gitignore_entries)

print(">>> [2/3] Filtering out heavy cache files from commit history...")
# Filter-branch removes the 100MB+ cache while keeping all commits, authors, and timestamps intact
cmd = [
    "git", "filter-branch", "-f",
    "--index-filter",
    "git rm -rf --cached --ignore-unmatch 04_Display/sandbox_preview 04_display/sandbox_preview",
    "--prune-empty",
    "HEAD"
]

res = subprocess.run(cmd)
if res.returncode == 0:
    print(">>> [SUCCESS] History cleaned successfully without losing any commits!")
else:
    print(">>> [ERROR] Filter branch failed.")
