import webview
import os

html_file = os.path.abspath(r"C:\Users\as712\ultron\04_display\orchestrator_hud.html")

# Create standalone Native Desktop Window
window = webview.create_window(
    title="ULTRON OS // QUANTUM INTERFACE",
    url=html_file,
    fullscreen=True,
    frameless=True,
    background_color='#010408'
)

webview.start()
