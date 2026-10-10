import os
import re

html_path = "C:\\Users\\as712\\ultron\\04_display\\ultron_mainframe.html"

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The NEW Ethereal Particle Hologram AI Code
    new_3d_code = """
        // --- 3D AUDIO-REACTIVE ETHEREAL HOLOGRAPHIC PARTICLE AI ---
        const container = document.getElementById('ai-canvas-container');
        const scene = new THREE.Scene();
        
        // Dark space fog to blend particles
        scene.fog = new THREE.FogExp2(0x010307, 0.015);

        const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.z = 45;

        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        // Boost pixel ratio for crisp particles
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        // Additive blending looks better with bright colors
        renderer.outputEncoding = THREE.sRGBEncoding;
        container.appendChild(renderer.domElement);

        // Group to hold the particle system
        const aiGroup = new THREE.Group();
        scene.add(aiGroup);

        // --- PARTICLE SWARM GENERATION ---
        const particleCount = 6000;
        const geometry = new THREE.BufferGeometry();
        const positions = new Float32Array(particleCount * 3);
        const originalPositions = new Float32Array(particleCount * 3);
        const randomPhases = new Float32Array(particleCount);
        const sizes = new Float32Array(particleCount);

        for (let i = 0; i < particleCount; i++) {
            // Generate points within a slightly elongated sphere (head shape)
            const u = Math.random();
            const v = Math.random();
            const theta = u * 2.0 * Math.PI;
            const phi = Math.acos(2.0 * v - 1.0);
            
            // Concentrate particles near the surface but leave some inside for volume
            const r = 8 + Math.pow(Math.random(), 2) * 4; 
            
            // Elongate Y-axis slightly for a "head" or "core" shape
            const x = r * Math.sin(phi) * Math.cos(theta);
            const y = (r * Math.sin(phi) * Math.sin(theta)) * 1.2; 
            const z = r * Math.cos(phi);

            positions[i * 3] = x;
            positions[i * 3 + 1] = y;
            positions[i * 3 + 2] = z;
            
            originalPositions[i * 3] = x;
            originalPositions[i * 3 + 1] = y;
            originalPositions[i * 3 + 2] = z;
            
            // Random phase for twinkling and breathing
            randomPhases[i] = Math.random() * Math.PI * 2;
            
            // Random particle sizes for depth
            sizes[i] = Math.random() * 0.15 + 0.05;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
        geometry.setAttribute('phase', new THREE.BufferAttribute(randomPhases, 1));

        // Create a custom shader material for glowing, twinkling particles
        const particleMaterial = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                color: { value: new THREE.Color(0x00f0ff) }, // Bright Cyan
                audioLevel: { value: 0 }
            },
            vertexShader: `
                uniform float time;
                uniform float audioLevel;
                attribute float size;
                attribute float phase;
                varying float vAlpha;
                
                void main() {
                    // Base breathing
                    float breathe = sin(time * 1.5 + phase) * 0.2;
                    
                    vec3 pos = position;
                    
                    // Audio reactivity (Lip Sync) - Lower Y vertices move more when speaking
                    float drop = 0.0;
                    if (pos.y < 0.0) {
                        drop = audioLevel * abs(pos.y) * 0.4;
                        // Add some chaotic vibration based on audio
                        pos.x += sin(time * 10.0 + phase) * audioLevel * 0.5;
                        pos.z += cos(time * 12.0 + phase) * audioLevel * 0.5;
                    }
                    pos.y -= drop;
                    
                    // Add global expansion based on audio
                    pos += normalize(pos) * (audioLevel * 1.5);

                    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
                    
                    // Particle size scales with audio and distance
                    gl_PointSize = size * (300.0 / -mvPosition.z) * (1.0 + audioLevel + breathe);
                    gl_Position = projectionMatrix * mvPosition;
                    
                    // Calculate alpha for twinkling
                    vAlpha = 0.4 + sin(time * 3.0 + phase) * 0.3 + (audioLevel * 0.5);
                }
            `,
            fragmentShader: `
                uniform vec3 color;
                varying float vAlpha;
                void main() {
                    // Make particles circular with soft edges
                    float dist = length(gl_PointCoord - vec2(0.5));
                    if (dist > 0.5) discard;
                    
                    // Soft glow center
                    float intensity = 1.0 - (dist * 2.0);
                    gl_FragColor = vec4(color, vAlpha * intensity);
                }
            `,
            transparent: true,
            blending: THREE.AdditiveBlending,
            depthWrite: false
        });

        const particleSwarm = new THREE.Points(geometry, particleMaterial);
        aiGroup.add(particleSwarm);

        // --- SUBTLE INNER GLOW ---
        // A faint, solid core inside the swarm to give it a center of mass
        const coreGeo = new THREE.SphereGeometry(6, 32, 32);
        const coreMat = new THREE.MeshBasicMaterial({ 
            color: 0x0088ff, 
            transparent: true, 
            opacity: 0.1,
            blending: THREE.AdditiveBlending
        });
        const innerCore = new THREE.Mesh(coreGeo, coreMat);
        innerCore.scale.set(1, 1.2, 1);
        aiGroup.add(innerCore);

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // --- LIP SYNC & AUDIO LOGIC ---
        let isSpeaking = false;
        let smoothedAudio = 0;

        const micBtn = document.getElementById('mic-btn');
        const aiStatus = document.getElementById('ai-status');
        
        micBtn.addEventListener('mousedown', () => { isSpeaking = true; micBtn.classList.add('listening'); aiStatus.innerText = "PROCESSING AUDIO..."; aiStatus.style.color = "#ffffff"; });
        micBtn.addEventListener('mouseup', () => { isSpeaking = false; micBtn.classList.remove('listening'); aiStatus.innerText = "ULTRON LISTENING..."; aiStatus.style.color = "#00ffaa"; });
        micBtn.addEventListener('mouseleave', () => { isSpeaking = false; micBtn.classList.remove('listening'); });

        const clock = new THREE.Clock();

        function animate() {
            requestAnimationFrame(animate);
            
            const elapsedTime = clock.getElapsedTime();
            
            // Smooth Audio Level transition
            let targetAudio = isSpeaking ? (Math.random() * 0.8 + 0.4) : 0; 
            smoothedAudio += (targetAudio - smoothedAudio) * 0.15;

            // Pass data to particle shader
            particleMaterial.uniforms.time.value = elapsedTime;
            particleMaterial.uniforms.audioLevel.value = smoothedAudio;

            // Slow, majestic rotation of the entire entity
            aiGroup.rotation.y = Math.sin(elapsedTime * 0.2) * 0.5;
            aiGroup.rotation.x = Math.cos(elapsedTime * 0.1) * 0.1;

            // Inner core pulses with audio
            innerCore.scale.setScalar(1 + smoothedAudio * 0.3);
            innerCore.material.opacity = 0.1 + (smoothedAudio * 0.2);

            // Shift color slightly when speaking (Cyan to brighter almost-white Cyan)
            const r = 0.0 + (smoothedAudio * 0.5);
            const g = 0.94 + (smoothedAudio * 0.06);
            const b = 1.0;
            particleMaterial.uniforms.color.value.setRGB(r, g, b);

            renderer.render(scene, camera);
        }
        animate();
    """

    # We use regex to replace ONLY the 3D code block, keeping everything else exactly the same.
    updated_content = re.sub(r'// --- NEW REALISTIC CINEMATIC 3D AI CORE ---.*?animate\(\);\s*</script>', new_3d_code + '\n    </script>', content, flags=re.DOTALL)

    # Backup attempt if the first regex doesn't match perfectly
    if updated_content == content:
        updated_content = re.sub(r'// --- 3D AUDIO-REACTIVE HOLOGRAPHIC AI ---.*?animate\(\);\s*</script>', new_3d_code + '\n    </script>', content, flags=re.DOTALL)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

import subprocess
subprocess.Popen(["python", "C:\\Users\\as712\\ultron\\04_display\\run_app.py"])
