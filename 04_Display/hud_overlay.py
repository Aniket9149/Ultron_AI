"""
ULTRON Neural Command Display (HUD Interface)
Provides a sci-fi desktop dashboard for interacting with Ultron and monitoring agent cores.
"""
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import urllib.request
import psutil

# Neon Color Palette
BG_DARK = "#0a0c10"
BG_CARD = "#12161f"
ACCENT_CYAN = "#00f0ff"
ACCENT_AMBER = "#ffaa00"
ACCENT_GREEN = "#00ff66"
ACCENT_RED = "#ff3344"
TEXT_MAIN = "#e0e6ed"
TEXT_MUTED = "#606c7d"
FONT_CODE = ("Consolas", 10)
FONT_HEAD = ("Segoe UI", 11, "bold")

class UltronHUD(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ULTRON // NEURAL COMMAND COCKPIT")
        self.geometry("1100x680")
        self.configure(bg=BG_DARK)
        self.minsize(900, 550)

        self._build_top_bar()
        self._build_main_body()
        self._build_bottom_bar()

        # Telemetry update thread
        self.is_running = True
        self.telemetry_thread = threading.Thread(target=self._telemetry_loop, daemon=True)
        self.telemetry_thread.start()

    def _build_top_bar(self):
        top_frame = tk.Frame(self, bg=BG_CARD, height=50, padx=15, pady=8)
        top_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(top_frame, text="ULTRON OS", font=("Segoe UI", 14, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        title_lbl.pack(side=tk.LEFT)

        sub_lbl = tk.Label(top_frame, text=" | AUTONOMOUS AGENT CORE v2.4", font=("Consolas", 10), fg=TEXT_MUTED, bg=BG_CARD)
        sub_lbl.pack(side=tk.LEFT, pady=(3, 0))

        # Status pills
        self.lm_status_lbl = tk.Label(top_frame, text="● LM-STUDIO: CHECKING", font=FONT_CODE, fg=ACCENT_AMBER, bg=BG_CARD)
        self.lm_status_lbl.pack(side=tk.RIGHT, padx=10)

        self.sys_status_lbl = tk.Label(top_frame, text="CPU: --% | RAM: --%", font=FONT_CODE, fg=ACCENT_CYAN, bg=BG_CARD)
        self.sys_status_lbl.pack(side=tk.RIGHT, padx=10)

    def _build_main_body(self):
        body = tk.Frame(self, bg=BG_DARK, padx=10, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        # Left Column: Agent Cortex Matrix
        left_col = tk.Frame(body, bg=BG_CARD, width=280, padx=12, pady=12, highlightbackground="#1b2230", highlightthickness=1)
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_col.pack_propagate(False)

        tk.Label(left_col, text="AGENT CORTEX MATRIX", font=FONT_HEAD, fg=ACCENT_CYAN, bg=BG_CARD).pack(anchor="w", pady=(0, 10))

        self.agents = {
            "ATLAS": ("Producer & High Architect", ACCENT_GREEN),
            "ARCHON": ("Engine & Workspace Sync", ACCENT_GREEN),
            "ULTRON_DEV": ("C# & Shader Programmer", ACCENT_AMBER),
            "AURA": ("Art, Light & Audio Director", ACCENT_CYAN),
            "CIPHER": ("Security & Quality Assurance", ACCENT_GREEN)
        }

        for agent, (role, color) in self.agents.items():
            box = tk.Frame(left_col, bg="#0d1117", padx=8, pady=6, highlightbackground="#1f2937", highlightthickness=1)
            box.pack(fill=tk.X, pady=4)
            
            top_line = tk.Frame(box, bg="#0d1117")
            top_line.pack(fill=tk.X)
            tk.Label(top_line, text=agent, font=("Segoe UI", 10, "bold"), fg=color, bg="#0d1117").pack(side=tk.LEFT)
            tk.Label(top_line, text="[ONLINE]", font=("Consolas", 8), fg=ACCENT_GREEN, bg="#0d1117").pack(side=tk.RIGHT)

            tk.Label(box, text=role, font=("Segoe UI", 8), fg=TEXT_MUTED, bg="#0d1117").pack(anchor="w", pady=(2, 0))

        # Quick Directives Frame
        tk.Label(left_col, text="QUICK ACTIONS", font=FONT_HEAD, fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w", pady=(20, 8))
        
        btn_clear = tk.Button(left_col, text="Flush Console Buffer", font=FONT_CODE, bg="#1a202c", fg=TEXT_MAIN,
                              activebackground=ACCENT_CYAN, activeforeground=BG_DARK, bd=0, pady=5, command=self._clear_logs)
        btn_clear.pack(fill=tk.X, pady=3)

        btn_ping = tk.Button(left_col, text="Probe Brain Latency", font=FONT_CODE, bg="#1a202c", fg=TEXT_MAIN,
                             activebackground=ACCENT_CYAN, activeforeground=BG_DARK, bd=0, pady=5, command=self._ping_lm_studio)
        btn_ping.pack(fill=tk.X, pady=3)

        # Right Column: Terminal Stream & Command Center
        right_col = tk.Frame(body, bg=BG_DARK)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Terminal Screen
        term_frame = tk.Frame(right_col, bg=BG_CARD, highlightbackground="#1b2230", highlightthickness=1)
        term_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tk.Label(term_frame, text=" LIVE TELEMETRY & AGENT CONSOLE", font=FONT_HEAD, fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w", padx=10, pady=8)

        self.console = scrolledtext.ScrolledText(
            term_frame, bg="#08090d", fg=TEXT_MAIN, font=FONT_CODE, insertbackground=ACCENT_CYAN,
            bd=0, padx=10, pady=10, highlightthickness=0
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Input Prompt Line
        input_frame = tk.Frame(right_col, bg=BG_CARD, height=45, padx=8, pady=8, highlightbackground="#1b2230", highlightthickness=1)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="DIRECTOR :>", font=FONT_CODE, fg=ACCENT_CYAN, bg=BG_CARD).pack(side=tk.LEFT, padx=(4, 8))

        self.cmd_entry = tk.Entry(input_frame, bg="#08090d", fg=TEXT_MAIN, font=FONT_CODE, insertbackground=ACCENT_CYAN, bd=0)
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8), ipady=4)
        self.cmd_entry.bind("<Return>", lambda event: self._send_command())

        send_btn = tk.Button(input_frame, text="TRANSMIT", font=("Segoe UI", 9, "bold"), bg=ACCENT_CYAN, fg=BG_DARK,
                             activebackground="#00b8c4", bd=0, padx=15, command=self._send_command)
        send_btn.pack(side=tk.RIGHT)

    def _build_bottom_bar(self):
        btm = tk.Frame(self, bg=BG_CARD, height=22, padx=12, pady=3)
        btm.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Label(btm, text="LOCATION: LOCALHOST:1234  |  SECURITY LEVEL: ROOT", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.LEFT)
        tk.Label(btm, text="ULTRON WORKSTATION ENGINE", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(side=tk.RIGHT)

    def log(self, text, color=TEXT_MAIN):
        self.console.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.console.see(tk.END)

    def _clear_logs(self):
        self.console.delete("1.0", tk.END)
        self.log("Buffer flushed cleanly.", ACCENT_CYAN)

    def _ping_lm_studio(self):
        threading.Thread(target=self._check_lm, daemon=True).start()

    def _check_lm(self):
        try:
            req = urllib.request.Request("http://127.0.0.1:1234/v1/models", headers={"User-Agent": "UltronHUD"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    self.lm_status_lbl.config(text="● LM-STUDIO: ONLINE", fg=ACCENT_GREEN)
                    self.log("LM Studio Core Pinged: 200 OK (Qwen Brain Online)", ACCENT_GREEN)
                    return
        except Exception:
            pass
        self.lm_status_lbl.config(text="● LM-STUDIO: OFFLINE", fg=ACCENT_RED)
        self.log("LM Studio ping failed. Check port 1234.", ACCENT_RED)

    def _telemetry_loop(self):
        self.log("ULTRON Neural Cockpit Initialized.", ACCENT_CYAN)
        self.log("Ready for high-level directives. Skill iteration is on pause.", TEXT_MUTED)
        self._check_lm()

        while self.is_running:
            try:
                cpu = psutil.cpu_percent(interval=None)
                ram = psutil.virtual_memory().percent
                self.sys_status_lbl.config(text=f"CPU: {cpu:.1f}% | RAM: {ram:.1f}%")
            except Exception:
                pass
            time.sleep(2.0)

    def _send_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        self.cmd_entry.delete(0, tk.END)
        self.log(f">> DIRECTOR: {cmd}", ACCENT_CYAN)
        
        # Ultron AI response thread
        threading.Thread(target=self._process_command, args=(cmd,), daemon=True).start()

    def _process_command(self, cmd):
        self.log("[ATLAS]: Parsing command intent...", TEXT_MUTED)
        time.sleep(0.4)
        self.log(f"[ULTRON]: Directive registered: '{cmd}'", ACCENT_AMBER)

if __name__ == "__main__":
    app = UltronHUD()
    app.mainloop()
