import os

sandbox_dir = r"C:\Users\as712\ultron\04_display\sandbox_preview"
preview_path = os.path.join(sandbox_dir, "preview_demo.html")
dock_path = os.path.join(sandbox_dir, "dock_sandbox.html")

# 1. FIX dock_sandbox.html
with open(dock_path, "r", encoding="utf-8") as f:
    dock_code = f.read()

# Make first tile clickable
if 'id="dock-tile-globe"' not in dock_code:
    # Replace first occurrence of dock-tile
    dock_code = dock_code.replace('<div class="dock-tile">', '<div class="dock-tile" id="dock-tile-globe" onclick="openGlobeHolo()">', 1)

if 'openGlobeHolo' not in dock_code:
    dock_script = """
<script>
  function openGlobeHolo() {
    try {
      const el = document.getElementById('dock-tile-globe');
      if (el) {
        el.classList.add('active');
        el.style.transform = 'scale(0.92)';
        setTimeout(() => { el.style.transform = ''; }, 150);
      }
      window.parent.postMessage({ type: 'OPEN_GLOBE_MODAL' }, '*');
    } catch(err) {
      console.error(err);
    }
  }
</script>
</body>
"""
    dock_code = dock_code.replace("</body>", dock_script)

with open(dock_path, "w", encoding="utf-8") as f:
    f.write(dock_code)
print("[OK] dock_sandbox.html updated!")

# 2. FIX preview_demo.html
with open(preview_path, "r", encoding="utf-8") as f:
    preview_code = f.read()

# Make sure dock points to dock_sandbox.html
preview_code = preview_code.replace("../component_center_dock.html", "dock_sandbox.html")

modal_container = """
  <!-- PLANETARY GLOBE TACTICAL MODAL OVERLAY -->
  <div id="globe-modal-container" style="display: none; position: fixed; inset: 0; z-index: 999999; background: rgba(0, 0, 0, 0.85); backdrop-filter: blur(12px); align-items: center; justify-content: center;">
    <iframe id="globe-modal-frame" src="modal_planetary_globe.html" style="width: 92vw; height: 90vh; border: 1px solid #00f0ff; border-radius: 6px; box-shadow: 0 0 55px rgba(0, 240, 255, 0.45); background: #02060d;"></iframe>
  </div>
</body>
"""

if 'id="globe-modal-container"' not in preview_code:
    preview_code = preview_code.replace("</body>", modal_container)

listener_logic = """
    // GLOBAL MESSAGE LISTENER FOR DOCK MODALS
    window.addEventListener('message', (e) => {
      if (e.data && e.data.type === 'OPEN_GLOBE_MODAL') {
        const mc = document.getElementById('globe-modal-container');
        if (mc) {
          mc.style.display = 'flex';
          const frame = document.getElementById('globe-modal-frame');
          if (frame && frame.contentWindow) frame.contentWindow.focus();
        }
      }
      if (e.data && e.data.type === 'CLOSE_GLOBE_MODAL') {
        const mc = document.getElementById('globe-modal-container');
        if (mc) mc.style.display = 'none';
        const dockIfr = document.querySelector('iframe[src*="dock"]');
        if (dockIfr && dockIfr.contentDocument) {
          const btn = dockIfr.contentDocument.getElementById('dock-tile-globe');
          if (btn) btn.classList.remove('active');
        }
      }
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const mc = document.getElementById('globe-modal-container');
        if (mc && mc.style.display === 'flex') {
          mc.style.display = 'none';
        }
      }
    });
</script>
"""

if "OPEN_GLOBE_MODAL" not in preview_code:
    preview_code = preview_code.replace("</script>", listener_logic)

with open(preview_path, "w", encoding="utf-8") as f:
    f.write(preview_code)
print("[OK] preview_demo.html updated with modal & listener!")
