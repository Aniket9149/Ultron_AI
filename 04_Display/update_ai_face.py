import os
import re

html_path = "C:\\Users\\as712\\ultron\\04_display\\ultron_mainframe.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The new Badass 3D AI Entity Code
    new_3d_code = """
        // --- 3D AUDIO-REACTIVE HOLOGRAPHIC AI ---
        const container = document.getElementById('ai-canvas-container');
        const scene = new THREE.Scene();
        
        // Add subtle fog for depth
        scene.fog = new THREE.FogExp2(0x010307, 0.015);

        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 50;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        container.appendChild(renderer.domElement);

        // Lighting for the Obsidian Look
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(ambientLight);
        
        const keyLight = new THREE.DirectionalLight(0x00f0ff, 2.5);
        keyLight.position.set(10, 10, 10);
        scene.add(keyLight);
        
        const rimLight = new THREE.PointLight(0x0088ff, 3.0, 50);
        rimLight.position.set(-10, -5, -10);
        scene.add(rimLight);

        // Group to hold everything
        const aiGroup = new THREE.Group();
        scene.add(aiGroup);

        // 1. The Inner Energy Core
        const coreGeo = new THREE.IcosahedronGeometry(6, 2);
        const coreMat = new THREE.MeshBasicMaterial({ 
            color: 0x00e5ff, 
            wireframe: true, 
            transparent: true, 
            opacity: 0.4 
        });
        const innerCore = new THREE.Mesh(coreGeo, coreMat);
        aiGroup.add(innerCore);

        // 2. The Shattered Obsidian Shards
        const shardsCount = 60;
        const shards = [];
        const shardGeo = new THREE.TetrahedronGeometry(2, 0);
        
        const shardMat = new THREE.MeshStandardMaterial({
            color: 0x050a14, // Very dark blue/black
            roughness: 0.2,
            metalness: 0.9,
            flatShading: true, // Gives that sharp, low-poly villain look
            emissive: 0x00e5ff,
            emissiveIntensity: 0.1
        });

        for(let i=0; i<shardsCount; i++) {
            const shard = new THREE.Mesh(shardGeo, shardMat);
            
            // Random position in a spherical shell
            const u = Math.random();
            const v = Math.random();
            const theta = u * 2.0 * Math.PI;
            const phi = Math.acos(2.0 * v - 1.0);
            const r = 10 + Math.random() * 4; // Distance from center
            
            shard.position.x = r * Math.sin(phi) * Math.cos(theta);
            shard.position.y = r * Math.sin(phi) * Math.sin(theta);
            shard.position.z = r * Math.cos(phi);
            
            // Random rotation
            shard.rotation.x = Math.random() * Math.PI;
            shard.rotation.y = Math.random() * Math.PI;
            shard.rotation.z = Math.random() * Math.PI;
            
            // Random scale
            const s = 0.5 + Math.random();
            shard.scale.set(s, s, s);
            
            // Store original data for animation
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

        // Lip Sync Simulation Logic
        let isSpeaking = false;
        let audioLevel = 0;

        const micBtn = document.getElementById('mic-btn');
        const aiStatus = document.getElementById('ai-status');
        
        micBtn.addEventListener('mousedown', () => { isSpeaking = true; micBtn.classList.add('listening'); aiStatus.innerText = "PROCESSING AUDIO..."; aiStatus.style.color = "#00f0ff"; });
        micBtn.addEventListener('mouseup', () => { isSpeaking = false; micBtn.classList.remove('listening'); aiStatus.innerText = "ULTRON LISTENING..."; aiStatus.style.color = "#00ffaa"; });
        micBtn.addEventListener('mouseleave', () => { isSpeaking = false; micBtn.classList.remove('listening'); });

        let time = 0;

        function animate() {
            requestAnimationFrame(animate);
            time += 0.02;

            let targetAudio = isSpeaking ? (Math.random() * 0.8 + 0.2) : 0;
            audioLevel += (targetAudio - audioLevel) * 0.15; 

            // Inner Core Animation
            innerCore.rotation.x += 0.01;
            innerCore.rotation.y += 0.015;
            innerCore.scale.setScalar(1 + audioLevel * 0.3); // Core expands when speaking

            // Outer Shards Animation
            shards.forEach(shard => {
                const data = shard.userData;
                
                // Idle floating
                const floatX = Math.sin(time * 2 + data.randomPhase) * 0.5;
                const floatY = Math.cos(time * 1.5 + data.randomPhase) * 0.5;
                
                // Audio reaction (Explosive expansion and shaking)
                const expansion = data.basePos.clone().normalize().multiplyScalar(audioLevel * 5);
                const shake = new THREE.Vector3(
                    (Math.random() - 0.5) * audioLevel,
                    (Math.random() - 0.5) * audioLevel,
                    (Math.random() - 0.5) * audioLevel
                );
                
                shard.position.copy(data.basePos).add(new THREE.Vector3(floatX, floatY, 0)).add(expansion).add(shake);
                
                // Shards rotate wildly when speaking
                shard.rotation.x = data.baseRot.x + time * 0.5 + audioLevel * Math.random();
                shard.rotation.y = data.baseRot.y + time * 0.3 + audioLevel * Math.random();
                
                // Emissive glow intensifies when speaking
                shard.material.emissiveIntensity = 0.1 + (audioLevel * 1.5);
            });

            // Whole group slow rotation
            aiGroup.rotation.y = Math.sin(time * 0.5) * 0.2;

            renderer.render(scene, camera);
        }
        animate();
    """

    # Replace the old 3D code block
    updated_content = re.sub(r'// --- 3D AUDIO-REACTIVE HOLOGRAPHIC AI ---.*?animate\(\);\s*</script>', new_3d_code + '\n    </script>', content, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

import subprocess
subprocess.Popen(["python", "C:\\Users\\as712\\ultron\\04_display\\run_app.py"])
