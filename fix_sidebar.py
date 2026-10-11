import os
import re

hud_path = os.path.join("04_Display", "orchestrator_hud.html")
if not os.path.exists(hud_path):
    hud_path = os.path.join("04_display", "orchestrator_hud.html")

print(f">>> Reading file: {hud_path}")
with open(hud_path, "r", encoding="utf-8") as f:
    html = f.read()

# Sidebar Interactive Styling
sidebar_css = """
<style id="ultron-sidebar-enhanced-css">
    /* High-priority click unblocker for sidebar elements */
    .sidebar, nav, [class*="sidebar"], [class*="nav"] {
        pointer-events: auto !important;
        z-index: 99999 !important;
    }

    /* All clickable items */
    .sidebar-active-tab {
        background: linear-gradient(90deg, rgba(0, 240, 255, 0.25) 0%, rgba(0, 102, 255, 0.15) 100%) !important;
        border-left: 3px solid #00f0ff !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.4) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
</style>
"""

# Dynamic Multi-Panel Switcher & Cyber Click Sound Script
sidebar_js = """
<script id="ultron-sidebar-functional-js">
document.addEventListener('DOMContentLoaded', () => {
    // 1. Futuristic Web-Audio Synthesized Chirp
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    function playCyberChirp(freq = 600) {
        try {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(freq * 1.5, audioCtx.currentTime + 0.05);
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.06);
        } catch(e) {}
    }

    // 2. Identify All Navigation Elements
    const navWords = ["HOME", "INTELLIGENCE", "AGENTS", "MEMORY", "SYSTEMS", "NETWORK", "TOOLS", "SETTINGS"];
    const allElements = document.querySelectorAll('*');
    const navBtns = [];

    allElements.forEach(el => {
        if (el.children.length <= 3) {
            const txt = el.innerText ? el.innerText.trim().toUpperCase() : '';
            navWords.forEach(word => {
                if (txt.startsWith(word) && !navBtns.some(b => b.el === el)) {
                    navBtns.push({ el: el, name: word });
                }
            });
        }
    });

    console.log(`[ULTRON HUD] Found ${navBtns.length} sidebar buttons.`);

    // 3. Bind Dynamic View Updates to Each Tab
    navBtns.forEach(btnObj => {
        const item = btnObj.el;
        const name = btnObj.name;
        
        item.style.cursor = 'pointer';
        item.style.pointerEvents = 'auto';
        item.style.transition = 'all 0.25s ease';

        item.addEventListener('click', (e) => {
            e.stopPropagation();
            playCyberChirp(750);

            // Toggle active glow
            navBtns.forEach(b => {
                b.el.classList.remove('sidebar-active-tab', 'active');
                b.el.style.borderColor = '';
            });
            item.classList.add('sidebar-active-tab');

            // Dynamic Panel Information Updates
            const overviewCard = document.querySelector('[class*="global-overview"], [class*="overview"]');
            const subTitle = document.querySelector('.sub-header, h2, h3');
            
            console.log(`>>> [ULTRON NAVIGATION] Switched to module: ${name}`);

            // Update Tactical Directive / Status if available
            const tacticBox = document.querySelector('[class*="tactical"]');
            if (tacticBox) {
                const badge = tacticBox.querySelector('span, .badge');
                if (badge) badge.innerText = `${name} // ENGAGED`;
            }
        });
    });

    // 4. Ensure START button always navigates to Mainframe
    const startBtns = document.querySelectorAll('*');
    startBtns.forEach(el => {
        if (el.innerText && el.innerText.trim().toUpperCase() === 'START') {
            el.style.cursor = 'pointer';
            el.style.pointerEvents = 'auto';
            el.style.zIndex = '999999';
            el.onclick = (e) => {
                e.preventDefault();
                playCyberChirp(900);
                console.log("[ULTRON] Transitioning to Quantum Mainframe...");
                window.location.href = 'ultron_mainframe.html';
            };
        }
    });
});
</script>
"""

# Clean old patches if present and inject fresh handlers
html = re.sub(r'<style id="ultron-sidebar-enhanced-css">.*?</style>', '', html, flags=re.DOTALL)
html = re.sub(r'<script id="ultron-sidebar-functional-js">.*?</script>', '', html, flags=re.DOTALL)

html = html.replace("</head>", sidebar_css + "\n</head>")
html = html.replace("</body>", sidebar_js + "\n</body>")

with open(hud_path, "w", encoding="utf-8") as f:
    f.write(html)

print(">>> [SUCCESS] orchestrator_hud.html sidebar logic & audio chirps installed!")
