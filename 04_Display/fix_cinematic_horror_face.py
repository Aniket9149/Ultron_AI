import os

html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON // HORRIFIC CINEMATIC AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@500;700&family=Chakra+Petch:wght@500;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; padding: 0; height: 100vh; background: #000000; color: #00f0ff;
            font-family: 'Chakra Petch', sans-serif; overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.03) 0%, transparent 80%);
        }
        
        .grid-bg { 
            position: absolute; inset: 0; 
            background-image: linear-gradient(rgba(0, 240, 255, 0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.015) 1px, transparent 1px); 
            background-size: 50px 50px; z-index: -1; perspective: 1000px; 
            transform: rotateX(60deg) translateY(-100px) scale(3); 
            animation: gridMove 15s linear infinite; 
        }
        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 50px; } }

        /* UI ELEMENTS */
        .top-bar { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.3); padding: 5px; border-radius: 8px; backdrop-filter: blur(10px); z-index: 100; }
        .mode-btn { padding: 8px 20px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 700; color: rgba(255, 255, 255, 0.6); cursor: pointer; border-radius: 4px; letter-spacing: 2px; transition: all 0.3s ease; border: 1px solid transparent; }
        .mode-btn.active { background: rgba(0, 240, 255, 0.15); color: #00f0ff; border: 1px solid #00f0ff; box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); }
        .back-hud { position: absolute; top: 20px; left: 20px; font-size: 11px; color: rgba(255,255,255,0.4); cursor: pointer; z-index: 100; letter-spacing: 2px; text-decoration: none; font-family: 'JetBrains Mono'; transition: color 0.3s; }
        .back-hud:hover { color: #ff0044; text-shadow: 0 0 8px #ff0044; }
        
        #ai-canvas-container { position: absolute; inset: 0; z-index: 10; filter: contrast(1.1) drop-shadow(0 0 30px rgba(0,240,255,0.1)); }

        .voice-status { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 100; }
        .status-text { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #00ffaa; letter-spacing: 3px; text-shadow: 0 0 10px #00ffaa; transition: all 0.3s ease; }
        .mic-btn { width: 60px; height: 60px; border-radius: 50%; background: rgba(0, 240, 255, 0.05); border: 2px solid #00f0ff; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 0 20px rgba(0, 240, 255, 0.15); transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter: blur(10px); }
        .mic-btn svg { width: 24px; height: 24px; fill: #00f0ff; transition: all 0.3s; }
        .mic-btn:active, .mic-btn.listening { background: rgba(255, 0, 68, 0.25); box-shadow: 0 0 35px #ff0044, inset 0 0 20px #ff0044; transform: scale(0.92); border-color: #ff0044; }
        .mic-btn.listening svg { fill: #ff0044; filter: drop-shadow(0 0 5px #ff0044); }

        #chat-panel { position: absolute; top: 80px; bottom: 40px; right: -450px; width: 400px; background: rgba(2, 6, 14, 0.85); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 12px; backdrop-filter: blur(20px); z-index: 150; display: flex; flex-direction: column; transition: right 0.4s ease; box-shadow: -10px 0 30px rgba(0, 0, 0, 0.8); }
        #chat-panel.open { right: 30px; }
        .chat-header { padding: 15px; border-bottom: 1px solid rgba(0, 240, 255, 0.2); font-family: 'Orbitron'; font-size: 12px; font-weight: 800; letter-spacing: 2px; color: #00f0ff; }
        .chat-history { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .msg { padding: 10px 14px; border-radius: 8px; font-size: 13px; max-width: 80%; line-height: 1.4; }
        .msg.user { align-self: flex-end; background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); color: #fff; }
        .msg.ai { align-self: flex-start; background: rgba(0, 255, 170, 0.05); border: 1px solid rgba(0, 255, 170, 0.2); color: #00ffaa; }
        .chat-input-area { padding: 15px; border-top: 1px solid rgba(0, 240, 255, 0.2); display: flex; gap: 10px; }
        .chat-input { flex: 1; background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 6px; padding: 10px 15px; color: #fff; font-family: 'Chakra Petch'; outline: none; }
        .send-btn { background: #00f0ff; border: none; border-radius: 6px; padding: 0 15px; color: #000; font-weight: bold; cursor: pointer; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="grid-bg"></div>
    <a class="back-hud" href="orchestrator_hud.html">[ < SYSTEM ABORT ]</a>

    <div class="top-bar">
        <div class="mode-btn active" id="btn-voice" onclick="setMode('VOICE')">NEURAL LINK</div>
        <div class="mode-btn" id="btn-chat" onclick="setMode('CHAT')">TEXT PROTOCOL</div>
    </div>

    <div id="ai-canvas-container"></div>

    <div class="voice-status">
        <div class="status-text" id="ai-status">ENTITY DORMANT...</div>
        <div class="mic-btn" id="mic-btn">
            <svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z"/></svg>
        </div>
    </div>

    <div id="chat-panel">
        <div class="chat-header">// NEURAL COM-LINK</div>
        <div class="chat-history">
            <div class="msg ai">Entity awakened. State your command.</div>
        </div>
        <div class="chat-input-area">
            <input type="text" class="chat-input" placeholder="Enter command...">
            <button class="send-btn">SEND</button>
        </div>
    </div>

    <script>
        function setMode(mode) {
            const chatPanel = document.getElementById('chat-panel');
            const btnVoice = document.getElementById('btn-voice');
            const btnChat = document.getElementById('btn-chat');
            const aiStatus = document.getElementById('ai-status');
            
            if (mode === 'CHAT') {
                chatPanel.classList.add('open'); btnChat.classList.add('active'); btnVoice.classList.remove('active');
                aiStatus.innerText = "TEXT INTERFACE ACTIVE"; aiStatus.style.color = "rgba(255,255,255,0.4)";
            } else {
                chatPanel.classList.remove('open'); btnVoice.classList.add('active'); btnChat.classList.remove('active');
                aiStatus.innerText = "ENTITY DORMANT..."; aiStatus.style.color = "#00ffaa";
            }
        }

        // ========================================================
        //  THE HORRIFIC PROCEDURAL LIQUID METAL SKULL (HIGH-POLY)
        // ========================================================
        const container = document.getElementById('ai-canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x000000, 0.015);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 0, 40);

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // --- CINEMATIC HORROR LIGHTING ---
        scene.add(new THREE.AmbientLight(0x0a0a0a)); // Very dark

        const topLight = new THREE.SpotLight(0x00f0ff, 5.0, 100, Math.PI/4, 0.5, 1);
        topLight.position.set(-15, 25, 20);
        scene.add(topLight);

        // Evil Crimson Rim Light (from below/back)
        const bloodLight = new THREE.SpotLight(0xff0033, 15.0, 100, Math.PI/2, 0.8, 1);
        bloodLight.position.set(20, -15, -20);
        scene.add(bloodLight);

        // Internal Mouth Glow
        const mouthGlow = new THREE.PointLight(0xff0000, 0, 20); // Starts at 0 intensity
        mouthGlow.position.set(0, -5, 5);
        scene.add(mouthGlow);

        const aiGroup = new THREE.Group();
        scene.add(aiGroup);

        // --- HIGH POLY PROCEDURAL MESH ---
        const radius = 9;
        // 256x256 segments = massive detail for liquid metal reflections
        const geometry = new THREE.SphereGeometry(radius, 256, 256);
        const pos = geometry.attributes.position;
        const originalPos = new Float32Array(pos.count * 3);

        // CARVE THE SKULL MATHEMATICALLY
        for (let i = 0; i < pos.count; i++) {
            let x = pos.getX(i);
            let y = pos.getY(i);
            let z = pos.getZ(i);

            // Narrow the temples
            x *= 0.85;

            // Taper and pull down the jaw
            if (y < 0) {
                x *= (1.0 + (y / radius) * 0.4); 
                y *= 1.1; // elongate jaw
            }

            // Slant forehead
            if (y > 3) z -= Math.pow(y - 3, 2) * 0.15;

            // Deep hollow eye sockets
            let dL = Math.hypot(x - (-3.2), y - 2);
            let dR = Math.hypot(x - 3.2, y - 2);
            if (dL < 2.8) z -= (2.8 - dL) * 2.5;
            if (dR < 2.8) z -= (2.8 - dR) * 2.5;

            // Nasal cavity indent
            let dN = Math.hypot(x, y - (-1.5));
            if (dN < 1.8) z -= (1.8 - dN) * 2.2;

            // Cheekbones protrusion
            if (Math.abs(x) > 3.5 && Math.abs(x) < 7 && y > -3 && y < 1.5) z += 1.2;

            // Apply corrupted/melted texture using mathematical noise
            let noise = Math.sin(x*1.5) * Math.cos(y*1.5) * Math.sin(z*1.5) * 0.6;
            z += noise;

            pos.setXYZ(i, x, y, z);
            originalPos[i*3] = x;
            originalPos[i*3+1] = y;
            originalPos[i*3+2] = z;
        }
        
        // Recalculate normals so lighting works perfectly on the deformed skull
        geometry.computeVertexNormals();

        // --- LIQUID METAL MATERIAL ---
        const material = new THREE.MeshPhysicalMaterial({
            color: 0x010203,       // Pitch black base
            metalness: 1.0,        // Pure metal
            roughness: 0.15,       // Glossy/wet look
            clearcoat: 1.0,        // Wet slime/liquid layer
            clearcoatRoughness: 0.1,
            wireframe: false
        });

        const skull = new THREE.Mesh(geometry, material);
        aiGroup.add(skull);

        // --- GLOWING EYES DEEP IN SOCKETS ---
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff });
        const eyeGeo = new THREE.SphereGeometry(0.7, 32, 32);
        
        const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
        eyeL.position.set(-3.2, 2.2, 4.0);
        // Scale Y to make them slanted/angry
        eyeL.scale.set(1, 0.4, 0.2);
        eyeL.rotation.z = -0.2;
        aiGroup.add(eyeL);

        const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
        eyeR.position.set(3.2, 2.2, 4.0);
        eyeR.scale.set(1, 0.4, 0.2);
        eyeR.rotation.z = 0.2;
        aiGroup.add(eyeR);

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight; 
            camera.updateProjectionMatrix(); 
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- HORRIFIC ANIMATION LOGIC ---
        let isSpeaking = false; let audioLevel = 0;
        const micBtn = document.getElementById('mic-btn');
        const aiStatus = document.getElementById('ai-status');

        micBtn.addEventListener('mousedown', () => { isSpeaking = true; micBtn.classList.add('listening'); aiStatus.innerText = "ENTITY AWAKE..."; aiStatus.style.color = "#ff0044"; });
        micBtn.addEventListener('mouseup', () => { isSpeaking = false; micBtn.classList.remove('listening'); aiStatus.innerText = "ENTITY DORMANT..."; aiStatus.style.color = "#00ffaa"; });
        micBtn.addEventListener('mouseleave', () => { isSpeaking = false; micBtn.classList.remove('listening'); });

        let time = 0;

        function animate() {
            requestAnimationFrame(animate);
            time += 0.02;

            let targetAudio = isSpeaking ? (Math.random() * 0.8 + 0.2) : 0;
            audioLevel += (targetAudio - audioLevel) * 0.15;

            // Idle Hover
            aiGroup.position.y = Math.sin(time * 1.5) * 0.5;
            aiGroup.rotation.y = Math.sin(time * 0.5) * 0.2;
            aiGroup.rotation.x = Math.cos(time * 0.4) * 0.1;

            // --- THE JAW TEARING EFFECT (LIP SYNC) ---
            const positions = geometry.attributes.position;
            let jawTearing = false;

            for (let i = 0; i < positions.count; i++) {
                let ox = originalPos[i*3];
                let oy = originalPos[i*3+1];
                let oz = originalPositions = originalPos[i*3+2]; // fix typo
                let ozReal = originalPos[i*3+2];

                let nx = ox;
                let ny = oy;
                let nz = ozReal;

                // If vertex is in the jaw/mouth area
                if (oy < -2) {
                    // Pull down based on audio
                    let drop = audioLevel * Math.pow(Math.abs(oy + 2), 1.2) * 0.4;
                    ny -= drop;

                    // HORROR GLITCH: When speaking, the mouth tears apart left/right and spazzes
                    let tear = Math.sin(nx * 15 + time * 30) * audioLevel * 0.4;
                    nx += tear * (oy < -4 ? 1 : 0.5); 
                    nz += tear * 0.5;
                }

                // Global heartbeat pulse
                let pulse = Math.sin(time * 3 + oy) * 0.02;
                nx += nx * pulse;
                nz += nz * pulse;

                positions.setXYZ(i, nx, ny, nz);
            }
            positions.needsUpdate = true;
            // Recalculate normals live so shadows dance across the torn metal
            geometry.computeVertexNormals();

            // --- LIGHTING & COLOR SHIFTS ---
            if(isSpeaking) {
                eyeMat.color.setHex(0xff0033); // Blood red eyes
                eyeL.scale.y = 0.4 + (audioLevel * 1.5);
                eyeR.scale.y = 0.4 + (audioLevel * 1.5);
                mouthGlow.intensity = audioLevel * 10.0; // Fire in the mouth
                aiGroup.position.z = (Math.random() - 0.5) * audioLevel * 0.5; // Violent shaking
            } else {
                eyeMat.color.setHex(0x00f0ff); // Calm cyan
                eyeL.scale.y = 0.4;
                eyeR.scale.y = 0.4;
                mouthGlow.intensity = 0;
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

# Force overwrite the ultron_mainframe.html
with open("ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

print("EPIC FIX DONE! Now run: python run_app.py")
