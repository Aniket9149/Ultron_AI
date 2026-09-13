"""
04_Display/hud_overlay.py
Non-blocking, thread-safe transparent screen HUD for Ultron OS visual states.
States: [IDLE | LISTENING | THINKING | EXECUTING | SPEAKING]
"""
from __future__ import annotations
import threading
import tkinter as tk
from typing import Optional

class UltronHUD:
    STATE_COLORS = {
        "IDLE": ("#111827", "#6B7280", "● IDLE"),
        "LISTENING": ("#064E3B", "#10B981", "◉ LISTENING..."),
        "THINKING": ("#1E3A8A", "#60A5FA", "⚙ THINKING..."),
        "EXECUTING": ("#78350F", "#F59E0B", "⚡ EXECUTING TASK"),
        "SPEAKING": ("#701A75", "#F472B6", "🔊 SPEAKING")
    }

    def __init__(self) -> None:
        self.root: Optional[tk.Tk] = None
        self.status_label: Optional[tk.Label] = None
        self.current_state = "IDLE"
        self._is_running = False
        self._thread: Optional[threading.Thread] = None

    def _build_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Ultron HUD")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.88)
        self.root.configure(bg="#0B0F19")

        screen_w = self.root.winfo_screenwidth()
        hud_w, hud_h = 240, 48
        pos_x = screen_w - hud_w - 24
        pos_y = 24
        self.root.geometry(f"{hud_w}x{hud_h}+{pos_x}+{pos_y}")

        container = tk.Frame(self.root, bg="#0B0F19", highlightthickness=1, highlightbackground="#374151")
        container.pack(fill="both", expand=True, padx=2, pady=2)

        title = tk.Label(
            container, text="ULTRON OS CORE", font=("Consolas", 7, "bold"),
            fg="#9CA3AF", bg="#0B0F19"
        )
        title.pack(anchor="w", padx=10, pady=(4, 0))

        self.status_label = tk.Label(
            container, text="● IDLE", font=("Consolas", 10, "bold"),
            fg="#6B7280", bg="#0B0F19"
        )
        self.status_label.pack(anchor="w", padx=10, pady=(0, 4))

        self._refresh_ui()
        self.root.mainloop()

    def start(self) -> None:
        if not self._is_running:
            self._is_running = True
            self._thread = threading.Thread(target=self._build_window, daemon=True)
            self._thread.start()

    def update_state(self, state: str) -> None:
        self.current_state = state.upper()
        if self.root and self.status_label:
            try:
                self.root.after(0, self._refresh_ui)
            except Exception:
                pass

    def _refresh_ui(self) -> None:
        if not self.status_label:
            return
        _, fg_col, display_text = self.STATE_COLORS.get(
            self.current_state, ("#111827", "#9CA3AF", f"● {self.current_state}")
        )
        self.status_label.config(text=display_text, fg=fg_col)

hud = UltronHUD()
