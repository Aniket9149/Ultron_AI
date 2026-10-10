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
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.1) 0%, transparent 60%);
        }
        
        /* 3D Grid Background */
        .grid-bg { 
            position: absolute; inset: 0; 
            background-image: linear-gradient(rgba(0, 240, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.05) 1px, transparent 1px); 
            background-size: 40px 40px; z-index: -1; perspective: 1000px; 
            transform: rotateX(60deg) translateY(-100px) scale(3); 
            animation: gridMove 10s linear infinite; 
        }
        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 40px; } }

        /* --------------------------------------
           STAGE 1: 3D HOLOGRAPHIC LOADER
        --------------------------------------- */
        #loader-stage {
            position: absolute; inset: 0; display: flex; flex-direction: column;
            align-items: center; justify-content: center; z-index: 50;
            transition: transform 0.8s cubic-bezier(0.8, 0, 0.2, 1), opacity 0.8s ease-in;
        }

        .gyro-loader {
            position: relative; width: 220px; height: 220px;
            transform-style: preserve-3d; perspective: 800px;
        }

        .gyro-ring {
            position: absolute; inset: 0; border-radius: 50%;
            border: 2px solid transparent;
            box-shadow: 0 0 20px rgba(0, 240, 255, 0.1), inset 0 0 20px rgba(0, 240, 255, 0.1);
        }

        .gyro-ring:nth-child(1) {
            border-top: 3px solid #00f0ff; border-bottom: 3px solid #00f0ff;
            animation: spin1 2s linear infinite;
        }
        .gyro-ring:nth-child(2) {
            width: 80%; height: 80%; top: 10%; left: 10%;
            border-left: 3px solid #00ffaa; border-right: 3px solid #00ffaa;
            animation: spin2 3s linear infinite;
        }
        .gyro-ring:nth-child(3) {
            width: 120%; height: 120%; top: -10%; left: -10%;
            border-top: 1px dashed rgba(0, 240, 255, 0.6); border-bottom: 1px dashed rgba(0, 240, 255, 0.6);
            animation: spin3 5s linear infinite;
        }

        @keyframes spin1 { 100% { transform: rotateX(65deg) rotateY(0deg) rotateZ(360deg); } }
        @keyframes spin2 { 100% { transform: rotateX(65deg) rotateY(45deg) rotateZ(-360deg); } }
        @keyframes spin3 { 100% { transform: rotateX(55deg) rotateY(-45deg) rotateZ(360deg); } }

        .loader-percent {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700;
            color: #ffffff; text-shadow: 0 0 15px #00f0ff; letter-spacing: 2px;
        }

        .loader-log {
            margin-top: 80px; font-family: 'JetBrains Mono', monospace; font-size: 11px;
            color: #8ba0b8; letter-spacing: 3px; height: 15px; text-transform: uppercase;
        }

        /* --------------------------------------
           STAGE 2: MAINFRAME CONTENT
        --------------------------------------- */
        #mainframe-stage {
            opacity: 0; transform: scale(1.1); pointer-events: none;
            transition: opacity 1.5s ease-out, transform 1.5s ease-out;
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            z-index: 10;
        }
        #mainframe-stage.active { opacity: 1; transform: scale(1); pointer-events: auto; }

        .core-text { 
            font-size: 50px; font-weight: 900; letter-spacing: 15px; 
            text-shadow: 0 0 30px rgba(0, 240, 255, 0.8), 0 0 60px rgba(0, 240, 255, 0.4); margin-bottom: 20px; 
        }
        .sub-text { font-family: 'JetBrains Mono', monospace; font-size: 14px; letter-spacing: 6px; color: #8ba0b8; }
        .sub-text span { color: #00ffaa; text-shadow: 0 0 10px #00ffaa; }
    </style>
</head>
<body>
    <div class="grid-bg"></div>

    <!-- STAGE 1: 3D LOADER -->
    <div id="loader-stage">
        <div class="gyro-loader">
            <div class="gyro-ring" style="transform: rotateX(65deg) rotateY(0deg);"></div>
            <div class="gyro-ring" style="transform: rotateX(65deg) rotateY(45deg);"></div>
            <div class="gyro-ring" style="transform: rotateX(55deg) rotateY(-45deg);"></div>
            <div class="loader-percent" id="pct-text">0%</div>
        </div>
        <div class="loader-log" id="log-text">INITIALIZING QUANTUM CORE...</div>
    </div>

    <!-- STAGE 2: MAINFRAME REVEAL -->
    <div id="mainframe-stage">
        <div class="core-text">ULTRON MAINFRAME</div>
        <div class="sub-text">SYSTEM STATUS: <span id="status-span">ONLINE & FULLY OPERATIONAL</span></div>
    </div>

    <script>
        const bootLogs = [
            "INITIALIZING QUANTUM CORE...",
            "BYPASSING SECURITY PROTOCOLS...",
            "DECRYPTING NEURAL MESH...",
            "SYNCING SATELLITE TELEMETRY...",
            "CALIBRATING HOLOGRAPHIC ENGINES...",
            "ACCESS GRANTED."
        ];
        
        const logEl = document.getElementById('log-text');
        const pctEl = document.getElementById('pct-text');
        const loaderStage = document.getElementById('loader-stage');
        const mainframeStage = document.getElementById('mainframe-stage');

        let progress = 0;
        let logIndex = 0;

        // LOADING SPEED KO SLOW KIYA GAYA HAI (120ms interval, aur random jumps chhote kiye hain)
        const bootInterval = setInterval(() => {
            progress += Math.floor(Math.random() * 3) + 1; 
            if (progress >= 100) progress = 100;
            
            pctEl.innerText = progress + '%';
            
            const expectedLog = Math.floor((progress / 100) * bootLogs.length);
            if (expectedLog > logIndex && expectedLog < bootLogs.length) {
                logIndex = expectedLog;
                logEl.innerText = bootLogs[logIndex];
            }

            if (progress === 100) {
                clearInterval(bootInterval);
                logEl.innerText = "SYSTEM ONLINE";
                logEl.style.color = "#00ffaa";
                pctEl.style.color = "#00ffaa";
                
                setTimeout(() => {
                    loaderStage.style.transform = 'scale(3)'; 
                    loaderStage.style.opacity = '0';          
                    
                    setTimeout(() => {
                        loaderStage.style.display = 'none';
                        mainframeStage.classList.add('active'); 
                    }, 800);
                }, 600);
            }
        }, 120); 
    </script>
</body>
</html>"""

with open("C:\\Users\\as712\\ultron\\04_display\\ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

import subprocess
subprocess.Popen(["python", "C:\\Users\\as712\\ultron\\04_display\\run_app.py"])
