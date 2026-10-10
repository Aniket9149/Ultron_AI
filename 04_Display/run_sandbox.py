import webview
import os
import http.server
import socketserver
import threading

PORT = 32888
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    def log_message(self, format, *args):
        pass

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

if __name__ == '__main__':
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    
    url = f"http://127.0.0.1:{PORT}/sandbox_preview/preview_demo.html"
    window = webview.create_window(
        title="ULTRON // SANDBOX LAB",
        url=url,
        fullscreen=True,
        frameless=True,
        easy_drag=True
    )
    webview.start(debug=False)
