# -*- coding: utf-8 -*-
"""
ULTRON SURFACE & WINDOW INSPECTOR (01_Sense)
Reads direct OS window handles. Zero optical hallucination.
"""
import pygetwindow as gw

class SurfaceInspector:
    def __init__(self):
        self.ignored_titles = [
            "", "Default IME", "MSCTFIME UI", "Program Manager", 
            "Settings", "Windows Input Experience"
        ]

    def get_active_window(self) -> str:
        """Returns the title of the currently focused foreground window."""
        get_active_window = getattr(gw, "getActiveWindow", None)
        if get_active_window is not None:
            win = get_active_window()
            return win.title.strip() if win and win.title else "Unknown"
        get_active_title = getattr(gw, "getActiveWindowTitle", None)
        title = get_active_title() if get_active_title is not None else ""
        return title.strip() if title else "Unknown"

    def get_running_surfaces(self) -> list:
        """Returns clean list of all non-minimized running application titles."""
        clean = []
        for w in gw.getAllWindows():
            t = w.title.strip()
            if t and t not in self.ignored_titles and len(t) > 2:
                if t not in clean and not w.isMinimized:
                    clean.append(t)
        return clean

    def summarize_view(self) -> str:
        """Constructs accurate grounded description of visible desktop surfaces."""
        active = self.get_active_window()
        open_apps = self.get_running_surfaces()
        
        if not open_apps:
            return "Screen par filhal koi major window active nahi hai."
        
        apps_str = ", ".join(open_apps[:4])
        return f"Currently active window '{active}' hai, aur samne ye apps open hain: {apps_str}."

surface_inspector = SurfaceInspector()
