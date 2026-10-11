import os
import sys
import time
import threading
import subprocess

def run_backend():
    try:
        import uvicorn
        uvicorn.run("ultron_bridge:app", host="127.0.0.1", port=8000, log_level="error")
    except Exception:
        pass

def find_edge():
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe")
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

if __name__ == "__main__":
    print(">>> [ULTRON OS] Booting Neural Backend Bridge...")
    b_thread = threading.Thread(target=run_backend, daemon=True)
    b_thread.start()
    time.sleep(0.8)

    ui_path = os.path.abspath(r"04_Display\orchestrator_hud.html")
    if not os.path.exists(ui_path):
        ui_path = os.path.abspath(r"04_display\orchestrator_hud.html")

    print(f">>> [ULTRON OS] Launching Desktop App with Blender 3D Permissions: {ui_path}")

    app_profile = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "ultron_desktop_app_profile")
    edge_exe = find_edge()
    file_url = f"file:///{ui_path.replace(os.sep, '/')}"

    if edge_exe:
        cmd = [
            edge_exe,
            f"--user-data-dir={app_profile}",
            f"--app={file_url}",
            "--allow-file-access-from-files",
            "--disable-web-security",
            "--start-fullscreen",
            "--kiosk",
            "--no-first-run",
            "--disable-default-apps"
        ]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass
    else:
        ps_cmd = f'Start-Process msedge -ArgumentList "--user-data-dir=`"{app_profile}`"", "--allow-file-access-from-files", "--app=`"{ui_path}`"", "--start-fullscreen"'
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd])

    print(">>> [ULTRON OS] Mainframe Terminated.")
