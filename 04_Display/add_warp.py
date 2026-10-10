import os

html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON // MAINFRAME</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; padding: 0; height: 100vh; background: #010307; color: #00f0ff;
            font-family: 'Orbitron', sans-serif; display: flex; flex-direction: column;
            align-items: center; justify-content: center; overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.15) 0%, transparent 60%);
            animation: fadeIn 2s ease-out;
        }
        @keyframes fadeIn { from { opacity: 0; transform: scale(1.1); filter: brightness(3); } to { opacity: 1; transform: scale(1); filter: brightness(1); } }
        
        .core-text { font-size: 50px; font-weight: 900; letter-spacing: 15px; text-shadow: 0 0 30px rgba(0, 240, 255, 0.8), 0 0 60px rgba(0, 240, 255, 0.4); margin-bottom: 20px; }
        .sub-text { font-family: 'JetBrains Mono', monospace; font-size: 14px; letter-spacing: 6px; color: #8ba0b8; }
        .sub-text span { color: #00ffaa; text-shadow: 0 0 10px #00ffaa; }
        
        .grid-bg { position: absolute; inset: 0; background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px); background-size: 40px 40px; z-index: -1; perspective: 1000px; transform: rotateX(60deg) translateY(-100px) scale(3); animation: gridMove 10s linear infinite; }
        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 40px; } }

        .back-btn {
            position: absolute; bottom: 50px; padding: 12px 30px; border: 1px solid rgba(0, 240, 255, 0.5);
            background: rgba(0, 240, 255, 0.05); color: #00f0ff; font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 3px; cursor: pointer; transition: all 0.3s;
        }
        .back-btn:hover { background: rgba(0, 240, 255, 0.2); box-shadow: 0 0 20px rgba(0, 240, 255, 0.5); }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="core-text">ULTRON MAINFRAME</div>
    <div class="sub-text">SYSTEM STATUS: <span>ONLINE & FULLY OPERATIONAL</span></div>
    
    <div class="back-btn" onclick="window.location.href='orchestrator_hud_review.html'">// REBOOT DASHBOARD</div>
</body>
</html>"""

with open("ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

transition_script = """
<!-- 3D WARP TRANSITION LOGIC -->
<script>
    function initiateUltronWarp() {
        const slab = document.getElementById('master-hologram-slab');
        const elements = document.querySelectorAll('.hud-element');
        const btn = document.querySelector('.ultron-start-btn');
        
        if(slab) {
            slab.style.perspective = '1500px';
            slab.style.transformStyle = 'preserve-3d';
        }
        
        if(btn) {
            btn.style.transition = 'opacity 0.2s';
            btn.style.opacity = '0';
        }

        if(elements) {
            elements.forEach((el, index) => {
                el.style.transition = `transform 1.2s cubic-bezier(0.7, 0, 0.2, 1) ${index * 0.05}s, opacity 0.8s ease-in ${index * 0.05}s, filter 0.8s ease-in`;
                el.style.transform = 'translateZ(1200px) scale(2)';
                el.style.opacity = '0';
                el.style.filter = 'blur(10px) brightness(2)';
            });
        }

        const flash = document.createElement('div');
        flash.style.cssText = 'position:fixed;inset:0;background:#00f0ff;opacity:0;z-index:9999999;pointer-events:none;transition:opacity 1.5s cubic-bezier(0.8,0,0.2,1);mix-blend-mode:screen;';
        document.body.appendChild(flash);

        setTimeout(() => { flash.style.opacity = '1'; }, 400);
        setTimeout(() => { window.location.href = 'ultron_mainframe.html'; }, 1400);
    }
</script>
<!-- END WARP TRANSITION LOGIC -->
"""

files_to_patch = ["orchestrator_hud_review.html", "orchestrator_hud.html"]

for file_path in files_to_patch:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        content = content.replace("console.log('ULTRON SYSTEM INITIATED')", "initiateUltronWarp()")
        
        if "initiateUltronWarp" not in content:
            content = content.replace("</body>", f"{transition_script}\n</body>")
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

import subprocess
subprocess.Popen(["python", "run_review.py"])
