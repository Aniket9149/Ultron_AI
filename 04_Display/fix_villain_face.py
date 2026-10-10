import os

html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON // MAIN AI INTERFACE</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@500;700&family=Chakra+Petch:wght@500;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; padding: 0; height: 100vh; background: #010307; color: #00f0ff;
            font-family: 'Chakra Petch', sans-serif; overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 80%);
        }
        
        .grid-bg { 
            position: absolute; inset: 0; 
            background-image: linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px); 
            background-size: 50px 50px; z-index: -1; perspective: 1000px; 
            transform: rotateX(60deg) translateY(-100px) scale(3); 
            animation: gridMove 15s linear infinite; 
        }
        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 50px; } }

        .top-bar {
            position: absolute; top: 20px; left: 50%; transform: translateX(-50%);
            display: flex; gap: 10px; background: rgba(0, 240, 255, 0.05);
            border: 1px solid rgba(0, 240, 255, 0.3); padding: 5px; border-radius: 8px;
            backdrop-filter: blur(10px); z-index: 100;
        }
        .mode-btn {
            padding: 8px 20px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 700;
            color: rgba(255, 255, 255, 0.6); cursor: pointer; border-radius: 4px; letter-spacing: 2px;
            transition: all 0.3s ease; border: 1px solid transparent;
        }
        .mode-btn.active {
            background: rgba(0, 240, 255, 0.15); color: #00f0ff;
            border: 1px solid #00f0ff; box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
        }

        #ai-canvas-container { position: absolute; inset: 0; z-index: 10; }

        .voice-status {
            position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
            display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 100;
        }
        .status-text {
            font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #00ffaa;
            letter-spacing: 3px; text-shadow: 0 0 10px #00ffaa;
        }
        .mic-btn {
            width: 60px; height: 60px; border-radius: 50%; background: rgba(0, 240, 255, 0.1);
            border: 2px solid #00f0ff; display: flex; justify-content: center; align-items: center;
            cursor: pointer; box-shadow: 0 0 20px rgba(0, 240, 255, 0.2); transition: all 0.2s;
        }
        .mic-btn svg { width: 24px; height: 24px; fill: #00f0ff; }
        .mic-btn:active, .mic-btn.listening {
            background: rgba(0, 240, 255, 0.3); box-shadow: 0 0 30px #00f0ff, inset 0 0 15px #00f0ff; transform: scale(0.95);
        }

        #chat-panel {
            position: absolute; top: 80px; bottom: 40px; right: -450px; width: 400px;
            background: rgba(2, 6, 14, 0.85); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 12px;
            backdrop-filter: blur(20px); z-index: 150; display: flex; flex-direction: column;
            transition: right 0.4s cubic-bezier(0.16, 1, 0.3, 1); box-shadow: -10px 0 30px rgba(0, 0, 0, 0.8);
        }
        #chat-panel.open { right: 30px; }
        
        .chat-header {
            padding: 15px; border-bottom: 1px solid rgba(0, 240, 255, 0.2); font-family: 'Orbitron';
            font-size: 12px; font-weight: 800; letter-spacing: 2px; color: #00f0ff;
        }
        .chat-history {
            flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px;
        }
        .msg { padding: 10px 14px; border-radius: 8px; font-size: 13px; max-width: 80%; line-height: 1.4; }
        .msg.user { align-self: flex-end; background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); color: #fff; }
        .msg.ai { align-self: flex-start; background: rgba(0, 255, 170, 0.05); border: 1px solid rgba(0, 255, 170, 0.2); color: #00ffaa; }
        
        .chat-input-area {
            padding: 15px; border-top: 1px solid rgba(0, 240, 255, 0.2); display: flex; gap: 10px;
        }
        .chat-input {
            flex: 1; background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(0, 240, 255, 0.3);
            border-radius: 6px; padding: 10px 15px; color: #fff; font-family: 'Chakra Petch'; outline: none;
        }
        .chat-input:focus { border-color: #00f0ff; box-shadow: 0 0 10px rgba(0, 240, 255, 0.3); }
        .send-btn {
            background: #00f0ff; border: none; border-radius: 6px; padding: 0 15px; color: #000;
            font-weight: bold; cursor: pointer;
        }

        .back-hud {
            position: absolute; top: 20px; left: 20px; font-size: 10px; color: rgba(255,255,255,0.5);
            cursor: pointer; z-index: 100; font-family: 'JetBrains Mono'; letter-spacing: 2px;
        }
        .back-hud:hover { color: #00f0ff; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="grid-bg"></div>

    <div class="back-hud" onclick="window.location.href='orchestrator_hud.html'">[ < RETURN TO DASHBOARD ]</div>

    <div class="top-bar">
        <div class="mode-btn active" id="btn-voice" onclick="setMode('VOICE')">VOICE LINK</div>
        <div class="mode-btn" id="btn-chat" onclick="setMode('CHAT')">TEXT CHAT</div>
    </div>

    <!-- SHATTERED OBSIDIAN 3D CORE RENDERS HERE -->
    <div id="ai-canvas-container"></div>

    <div class="voice-status">
        <div class="status-text" id="ai-status">ULTRON LISTENING...</div>
        <div class="mic-btn" id="mic-btn">
            <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z"/></svg>
        </div>
    </div>

    <div id="chat-panel">
        <div class="chat-header">// NEURAL COM-LINK</div>
        <div class="chat-history">
            <div class="msg ai">Connection established. How can I assist you today?</div>
            <div class="msg user">Analyze current sector threat levels.</div>
            <div class="msg ai">Scanning... All parameters normal. No immediate threats detected.</div>
        </div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" placeholder="Enter command...">
            <button class="send-btn">SEND</button>
        </div>
    </div>

    <script>
        const chatPanel = document.getElementById('chat-panel');
        const btnVoice = document.getElementById('btn-voice');
        const btnChat = document.getElementById('btn-chat');
        const aiStatus = document.getElementById('ai-status');

        function setMode(mode) {
            if (mode === 'CHAT') {
                chatPanel.classList.add('open');
                btnChat.classList.add('active');
                btnVoice.classList.remove('active');
                aiStatus.innerText = "TEXT INTERFACE ACTIVE";
            } else {
                chatPanel.classList.remove('open');
                btnVoice.classList.add('active');
                btnChat.classList.remove('active');
                aiStatus.innerText = "ULTRON LISTENING...";
            }
        }

        // --- NEW BADASS VILLAIN AI CORE ---
        const container = document.getElementById('ai-canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x010307, 0.015);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 50;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // Moody Lighting
        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        const keyLight = new THREE.DirectionalLight(0x00f0ff, 2.5);
        keyLight.position.set(10, 10, 10);
        scene.add(keyLight);
        const rimLight = new THREE.PointLight(0x0088ff, 3.0, 50);
        rimLight.position.set(-10, -5, -10);
        scene.add(rimLight);

        const aiGroup = new THREE.Group();
        scene.add(aiGroup);

        // 1. Inner Glowing Energy Core
        const coreGeo = new THREE.IcosahedronGeometry(5, 2);
        const coreMat = new THREE.MeshBasicMaterial({ 
            color: 0x00e5ff, wireframe: true, transparent: true, opacity: 0.4 
        });
        const innerCore = new THREE.Mesh(coreGeo, coreMat);
        aiGroup.add(innerCore);

        // 2. The Shattered Dark Metal Shards
        const shards = [];
        const shardGeo = new THREE.TetrahedronGeometry(2.5, 0);
        const shardMat = new THREE.MeshStandardMaterial({
            color: 0x02050a, // Dark void metal
            roughness: 0.2, metalness: 0.9, flatShading: true,
            emissive: 0x00e5ff, emissiveIntensity: 0.1
        });

        for(let i=0; i<80; i++) {
            const shard = new THREE.Mesh(shardGeo, shardMat);
            const u = Math.random(), v = Math.random();
            const theta = u * 2.0 * Math.PI;
            const phi = Math.acos(2.0 * v - 1.0);
            const r = 9 + Math.random() * 5; 
            
            shard.position.set(r * Math.sin(phi) * Math.cos(theta), r * Math.sin(phi) * Math.sin(theta), r * Math.cos(phi));
            shard.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
            
            const s = 0.5 + Math.random();
            shard.scale.set(s, s, s);
            
            shard.userData = {
                basePos: shard.position.clone(),
                baseRot: shard.rotation.clone(),
                randomPhase: Math.random() * 100
            };
            
            shards.push(shard);
            aiGroup.add(shard);
        }

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        let isSpeaking = false;
        let audioLevel = 0;

        const micBtn = document.getElementById('mic-btn');
        micBtn.addEventListener('mousedown', () => { isSpeaking = true; micBtn.classList.add('listening'); aiStatus.innerText = "PROCESSING AUDIO..."; aiStatus.style.color = "#00f0ff"; });
        micBtn.addEventListener('mouseup', () => { isSpeaking = false; micBtn.classList.remove('listening'); aiStatus.innerText = "ULTRON LISTENING..."; aiStatus.style.color = "#00ffaa"; });
        micBtn.addEventListener('mouseleave', () => { isSpeaking = false; micBtn.classList.remove('listening'); });

        let time = 0;

        function animate() {
            requestAnimationFrame(animate);
            time += 0.02;

            let targetAudio = isSpeaking ? (Math.random() * 0.8 + 0.3) : 0;
            audioLevel += (targetAudio - audioLevel) * 0.15; 

            innerCore.rotation.x += 0.01;
            innerCore.rotation.y += 0.015;
            innerCore.scale.setScalar(1 + audioLevel * 0.4); 

            shards.forEach(shard => {
                const data = shard.userData;
                const floatX = Math.sin(time * 2 + data.randomPhase) * 0.5;
                const floatY = Math.cos(time * 1.5 + data.randomPhase) * 0.5;
                
                // Explode outward on talk
                const expansion = data.basePos.clone().normalize().multiplyScalar(audioLevel * 6);
                const shake = new THREE.Vector3((Math.random()-0.5)*audioLevel, (Math.random()-0.5)*audioLevel, (Math.random()-0.5)*audioLevel);
                
                shard.position.copy(data.basePos).add(new THREE.Vector3(floatX, floatY, 0)).add(expansion).add(shake);
                
                shard.rotation.x = data.baseRot.x + time * 0.5 + audioLevel * Math.random();
                shard.rotation.y = data.baseRot.y + time * 0.3 + audioLevel * Math.random();
                
                shard.material.emissiveIntensity = 0.1 + (audioLevel * 2.0);
            });

            aiGroup.rotation.y = Math.sin(time * 0.5) * 0.2;

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>"""

with open("C:\\Users\\as712\\ultron\\04_display\\ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

import subprocess
subprocess.Popen(["python", "C:\\Users\\as712\\ultron\\04_display\\run_app.py"])
