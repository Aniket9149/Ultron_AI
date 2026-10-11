import os

hud_path = os.path.join("04_Display", "orchestrator_hud.html")
if not os.path.exists(hud_path):
    hud_path = os.path.join("04_display", "orchestrator_hud.html")

print(f">>> Reading: {hud_path}")
with open(hud_path, "r", encoding="utf-8") as f:
    content = f.read()

css_fix = """
<style id="ultron-click-fix">
    .sidebar, .nav-item, nav, .start-btn, #start-btn, button, .action-btn {
        pointer-events: auto !important;
        position: relative !important;
        z-index: 999999 !important;
        cursor: pointer !important;
    }
    iframe, canvas {
        pointer-events: none !important;
    }
    .interactive-panel {
        pointer-events: auto !important;
    }
</style>
"""

js_fix = """
<script id="ultron-nav-fix">
    document.addEventListener('DOMContentLoaded', () => {
        const startBtns = document.querySelectorAll('#start-btn, .start-btn, button');
        startBtns.forEach(btn => {
            if (btn.innerText.includes('START') || btn.id === 'start-btn' || btn.classList.contains('start-btn')) {
                btn.onclick = (e) => {
                    e.preventDefault();
                    console.log("[ULTRON] Launching Mainframe...");
                    window.location.href = 'ultron_mainframe.html';
                };
            }
        });
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.onclick = function() {
                navItems.forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            };
        });
    });
</script>
"""

if "ultron-click-fix" not in content:
    content = content.replace("</head>", css_fix + "\n</head>")

if "ultron-nav-fix" not in content:
    content = content.replace("</body>", js_fix + "\n</body>")

with open(hud_path, "w", encoding="utf-8") as f:
    f.write(content)

print(">>> [SUCCESS] orchestrator_hud.html patched!")

# Update run_app.py for local server (CORS Fix)
run_app_path = os.path.join("04_Display", "run_app.py")
if not os.path.exists(run_app_path):
    run_app_path = os.path.join("04_display", "run_app.py")

server_code = '''import webview
import http.server
import socketserver
import threading
import os

PORT = 8088
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    print(">>> [ULTRON OS] Initializing Local Neural Server on port 8088...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    url = f"http://localhost:{PORT}/orchestrator_hud.html"
    print(f">>> [ULTRON OS] Launching Ultron UI: {url}")

    window = webview.create_window(
        title="ULTRON // QUANTUM AI MAINFRAME",
        url=url,
        width=1440,
        height=900,
        resizable=True,
        frameless=False,
        background_color='#010307'
    )
    webview.start(debug=False)
    print(">>> [ULTRON OS] Mainframe Terminated.")
'''

with open(run_app_path, "w", encoding="utf-8") as f:
    f.write(server_code)

print(">>> [SUCCESS] run_app.py updated with HTTP server mode!")
