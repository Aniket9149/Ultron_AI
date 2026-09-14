from flask import Flask, render_template, jsonify, request
import threading
import psutil
import requests
import webview
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "assets"),
    static_url_path="/static"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/telemetry')
def telemetry():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent
    })

def run_flask():
    app.run(host="127.0.0.1", port=5055, debug=False, use_reloader=False)

if __name__ == "__main__":
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()
    
    webview.create_window(
        title="ULTRON // AI OPERATING SYSTEM",
        url="http://127.0.0.1:5055",
        width=1340,
        height=780,
        resizable=True,
        background_color="#030508"
    )
    webview.start()
