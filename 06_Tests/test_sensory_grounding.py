# -*- coding: utf-8 -*-
from importlib.machinery import SourceFileLoader

print("=== VERIFYING ULTRON SENSORY INSPECTION ===")

inspector = SourceFileLoader('surface_inspector', '01_Sense/surface_inspector.py').load_module().surface_inspector
grounding = SourceFileLoader('native_grounding', '01_Sense/native_grounding.py').load_module().native_grounding

print("\n1. Active Window Title:")
print(">>", inspector.get_active_window())

print("\n2. Ground-Truth Visible Windows List:")
print(">>", inspector.get_running_surfaces())

print("\n3. Verbal Screen Summary:")
print(">>", inspector.summarize_view())

print("\n4. Testing Accessibility Tree Scan (New Tab button check):")
coords = grounding.get_new_tab_button()
print(">> Found browser tab coords:", coords if coords else "Browser not open / tab not in foreground")

print("\n[SUCCESS]: Sensory grounding test complete.")
