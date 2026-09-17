import webview
import os

target = os.path.abspath(r"orchestrator_hud_review.html")

window = webview.create_window(
    title="ULTRON OS // LIVE REVIEW ENVIRONMENT",
    url=target,
    fullscreen=True,
    frameless=True,
    background_color='#010408'
)

webview.start()
