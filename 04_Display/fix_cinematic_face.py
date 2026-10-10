import os

html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRON // CINEMATIC AI INTERFACE</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=JetBrains+Mono:wght@500;700&family=Chakra+Petch:wght@500;600&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0; padding: 0; height: 100vh; background: #010307; color: #00f0ff;
            font-family: 'Chakra Petch', sans-serif; overflow: hidden;
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.05) 0%, transparent 80%);
        }
        
        .grid-bg { 
            position: absolute; inset: 0; 
            background-image: linear-gradient(rgba(0, 240, 255, 0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 240, 255, 0.02) 1px, transparent 1px); 
            background-size: 50px 50px; z-index: -1; perspective: 1000px; 
            transform: rotateX(60deg) translateY(-100px) scale(3); 
            animation: gridMove 15s linear infinite; 
        }
        @keyframes gridMove { from { background-position: 0 0; } to { background-position: 0 50px; } }

        /* UI ELEMENTS */
        .top-bar { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); display: flex; gap: 10px; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.3); padding: 5px; border-radius: 8px; backdrop-filter: blur(10px); z-index: 100; }
        .mode-btn { padding: 8px 20px; font-family: 'Orbitron', sans-serif; font-size: 11px; font-weight: 700; color: rgba(255, 255, 255, 0.6); cursor: pointer; border-radius: 4px; letter-spacing: 2px; transition: all 0.3s ease; border: 1px solid transparent; }
        .mode-btn.active { background: rgba(0, 240, 255, 0.15); color: #00f0ff; border: 1px solid #00f0ff; box-shadow: 0 0 15px rgba(0, 240, 255, 0.4); }
        .back-hud { position: absolute; top: 20px; left: 20px; font-size: 11px; color: rgba(255,255,255,0.6); cursor: pointer; z-index: 100; letter-spacing: 2px; text-decoration: none; font-family: 'JetBrains Mono'; }
        .back-hud:hover { color: #00f0ff; text-shadow: 0 0 8px #00f0ff; }
        
        #ai-canvas-container { position: absolute; inset: 0; z-index: 10; }

        .voice-status { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; gap: 10px; z-index: 100; }
        .status-text { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #00ffaa; letter-spacing: 3px; text-shadow: 0 0 10px #00ffaa; transition: all 0.3s ease; }
        .mic-btn { width: 60px; height: 60px; border-radius: 50%; background: rgba(0, 240, 255, 0.05); border: 2px solid #00f0ff; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 0 20px rgba(0, 240, 255, 0.15); transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter: blur(10px); }
        .mic-btn svg { width: 24px; height: 24px; fill: #00f0ff; transition: all 0.3s; }
        .mic-btn:active, .mic-btn.listening { background: rgba(0, 240, 255, 0.25); box-shadow: 0 0 35px #00f0ff, inset 0 0 20px #00f0ff; transform: scale(0.92); border-color: #ffffff; }
        .mic-btn.listening svg { fill: #ffffff; filter: drop-shadow(0 0 5px #ffffff); }

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
    <a class="back-hud" href="orchestrator_hud.html">[ < RETURN TO DASHBOARD ]</a>

    <div class="top-bar">
        <div class="mode-btn active" id="btn-voice" onclick="setMode('VOICE')">VOICE LINK</div>
        <div class="mode-btn" id="btn-chat" onclick="setMode('CHAT')">TEXT CHAT</div>
    </div>

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
                aiStatus.innerText = "ULTRON LISTENING..."; aiStatus.style.color = "#00ffaa";
            }
        }

        // --- CINEMATIC FACETED ARMOR AI ENGINE ---
        const container = document.getElementById('ai-canvas-container');
        const scene = new THREE.Scene();
        scene.fog = new THREE.FogExp2(0x010307, 0.015);

        const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 45;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // --- CINEMATIC LIGHTING ---
        scene.add(new THREE.AmbientLight(0xffffff, 0.1)); // Deep shadows

        const mainLight = new THREE.SpotLight(0x00f0ff, 6); // Intense Cyan
        mainLight.position.set(15, 20, 20);
        mainLight.penumbra = 0.5;
        scene.add(mainLight);

        const rimLight = new THREE.SpotLight(0xff0044, 8); // Villain Red/Pink Rim Light
        rimLight.position.set(-20, 10, -20);
        rimLight.penumbra = 0.5;
        scene.add(rimLight);

        const bottomLight = new THREE.PointLight(0x00ffaa, 3, 50); // Toxic green underglow
        bottomLight.position.set(0, -15, 5);
        scene.add(bottomLight);

        const aiGroup = new THREE.Group();
        scene.add(aiGroup);

        // --- MATERIALS ---
        const armorMat = new THREE.MeshPhysicalMaterial({
            color: 0x050a12, metalness: 0.9, roughness: 0.3,
            clearcoat: 1.0, clearcoatRoughness: 0.1, flatShading: true // Stealth bomber faceted look
        });
        const edgeMat = new THREE.LineBasicMaterial({ color: 0x00f0ff, transparent: true, opacity: 0.4 });
        const eyeMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });

        function createArmorPlate(geo, x, y, z, rx, ry, rz) {
            const mesh = new THREE.Mesh(geo, armorMat);
            mesh.position.set(x, y, z);
            mesh.rotation.set(rx, ry, rz);
            
            const edges = new THREE.EdgesGeometry(geo);
            const line = new THREE.LineSegments(edges, edgeMat);
            mesh.add(line);
            
            aiGroup.add(mesh);
            return mesh;
        }

        // --- BUILD THE MASK ---
        // 1. Cranium (Crown)
        createArmorPlate(new THREE.CylinderGeometry(5.5, 5, 6, 6), 0, 5, 0, 0, 0, 0);

        // 2. Forehead Guard
        createArmorPlate(new THREE.BoxGeometry(8, 2.5, 3), 0, 3.5, 3.5, 0.2, 0, 0);

        // 3. Cheeks
        createArmorPlate(new THREE.BoxGeometry(3.5, 8, 3.5), -4.5, -1, 1.5, 0, -0.4, -0.3);
        createArmorPlate(new THREE.BoxGeometry(3.5, 8, 3.5), 4.5, -1, 1.5, 0, 0.4, 0.3);

        // 4. Nose Bridge (Sharp)
        createArmorPlate(new THREE.CylinderGeometry(1.5, 2.5, 5, 3), 0, 0.5, 4.2, -0.2, 0, 0);

        // 5. Ear / Side Vents
        createArmorPlate(new THREE.CylinderGeometry(2.5, 2.5, 2, 8), -6, 2, -1, 0, 0, Math.PI/2);
        createArmorPlate(new THREE.CylinderGeometry(2.5, 2.5, 2, 8), 6, 2, -1, 0, 0, Math.PI/2);

        // 6. Mechanical Jaw (Hinged Group)
        const jawGroup = new THREE.Group();
        jawGroup.position.set(0, -1, 2); // Hinge pivot point
        
        const jawMesh = new THREE.Mesh(new THREE.CylinderGeometry(4, 2, 4, 6), armorMat);
        jawMesh.position.set(0, -2.5, 0);
        jawMesh.rotation.set(0.1, 0, 0);
        const jawEdges = new THREE.EdgesGeometry(new THREE.CylinderGeometry(4, 2, 4, 6));
        jawMesh.add(new THREE.LineSegments(jawEdges, edgeMat));
        jawGroup.add(jawMesh);
        aiGroup.add(jawGroup);

        // 7. ANGRY GLOWING EYES (Slits, not circles)
        const eyeL = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.35, 0.1), eyeMat);
        eyeL.position.set(-2.5, 2.6, 5.0);
        eyeL.rotation.set(0, -0.2, 0.2); // Angry downward tilt
        aiGroup.add(eyeL);

        const eyeR = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.35, 0.1), eyeMat);
        eyeR.position.set(2.5, 2.6, 5.0);
        eyeR.rotation.set(0, 0.2, -0.2); // Angry downward tilt
        aiGroup.add(eyeR);

        // Inner glowing core visible behind the mask gaps
        const coreMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.15 });
        const core = new THREE.Mesh(new THREE.IcosahedronGeometry(4.5, 2), coreMat);
        core.position.set(0, 1, 0);
        aiGroup.add(core);

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight; 
            camera.updateProjectionMatrix(); 
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- ANIMATION & REAL JAW LIP-SYNC ---
        let isSpeaking = false; let audioLevel = 0;
        const micBtn = document.getElementById('mic-btn');
        micBtn.addEventListener('mousedown', () => { isSpeaking = true; micBtn.classList.add('listening'); aiStatus.innerText = "PROCESSING AUDIO..."; aiStatus.style.color = "#ffffff"; });
        micBtn.addEventListener('mouseup', () => { isSpeaking = false; micBtn.classList.remove('listening'); aiStatus.innerText = "ULTRON LISTENING..."; aiStatus.style.color = "#00ffaa"; });
        micBtn.addEventListener('mouseleave', () => { isSpeaking = false; micBtn.classList.remove('listening'); });

        let time = 0;

        function animate() {
            requestAnimationFrame(animate);
            time += 0.03;

            let targetAudio = isSpeaking ? (Math.random() * 0.8 + 0.2) : 0;
            audioLevel += (targetAudio - audioLevel) * 0.15;

            // Idle Cinematic Hover
            aiGroup.position.y = Math.sin(time * 1.5) * 0.5;
            aiGroup.rotation.y = Math.sin(time * 0.5) * 0.2;
            aiGroup.rotation.x = Math.cos(time * 0.4) * 0.05;

            // REAL JAW DROP
            // Jaw physically hinges downward when speaking
            jawGroup.rotation.x = -(audioLevel * 0.4);

            // Eye intensity & color change
            eyeL.scale.y = 1 + (audioLevel * 1.5);
            eyeR.scale.y = 1 + (audioLevel * 1.5);
            
            if(isSpeaking) {
                eyeMat.color.setHex(0x00ffaa); // Toxic Green eyes when talking
                edgeMat.color.setHex(0x00ffaa);
                coreMat.opacity = 0.3 + (audioLevel * 0.3);
            } else {
                eyeMat.color.setHex(0x00ffff); // Cyan idle
                edgeMat.color.setHex(0x00f0ff);
                coreMat.opacity = 0.15;
            }

            core.rotation.y -= 0.01;

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

with open("C:\\Users\\as712\\ultron\\04_display\\ultron_mainframe.html", "w", encoding="utf-8") as f:
    f.write(html_page)

# Cache buster to ensure the new HTML loads immediately
orchestrator_path = "C:\\Users\\as712\\ultron\\04_display\\orchestrator_hud.html"
if os.path.exists(orchestrator_path):
    with open(orchestrator_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    content = re.sub(r"window\.location\.href\s*=\s*'ultron_mainframe\.html(\?v=\d+)?'", "window.location.href = 'ultron_mainframe.html?v=' + Date.now()", content)
    
    with open(orchestrator_path, "w", encoding="utf-8") as f:
        f.write(content)
