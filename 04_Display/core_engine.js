// =========================================================
// ULTRON OS - 3D QUANTUM CORE ENGINE (MODULAR MODULE)
// =========================================================

class QuantumCoreEngine {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.composer = null;
    this.controls = null;
    this.clock = new THREE.Clock();

    // Groups & Meshes
    this.masterGroup = new THREE.Group();
    this.gimbals = [];
    this.particles = null;
    this.particleOrbits = [];
    this.singularityMesh = null;
    this.haloMesh = null;
    this.obsidianCrystal = null;
    this.crystalWire = null;
    this.fireRing = null;
    this.fireShaderMat = null;

    // Mouse Interaction
    this.mouseX = 0;
    this.mouseY = 0;
    this.targetX = 0;
    this.targetY = 0;

    this.init();
  }

  init() {
    this.initScene();
    this.initLightsAndEnvironment();
    this.buildCoreSingularity();
    this.buildPlasmaRings();
    this.buildHeavyGimbals();
    this.buildParticles();
    this.initPostProcessing();
    this.initEvents();
    this.animate();
  }

  initScene() {
    this.scene = new THREE.Scene();
    
    // Balanced Close-up Cinematic Framing
    this.camera = new THREE.PerspectiveCamera(38, window.innerWidth / window.innerHeight, 0.1, 100);
    this.camera.position.set(0, 1.2, 5.5);

    this.renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.25;
    this.container.appendChild(this.renderer.domElement);

    this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 3.2;
    this.controls.maxDistance = 12.0;

    this.scene.add(this.masterGroup);
  }

  initLightsAndEnvironment() {
    // Procedural Studio Reflection Canvas
    const cv = document.createElement('canvas');
    cv.width = 1024; cv.height = 512;
    const ctx = cv.getContext('2d');
    const bg = ctx.createLinearGradient(0, 0, 0, 512);
    bg.addColorStop(0, '#040d18');
    bg.addColorStop(0.5, '#010408');
    bg.addColorStop(1, '#050209');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, 1024, 512);

    ctx.fillStyle = '#1e3852';
    ctx.fillRect(150, 60, 260, 80);
    ctx.fillStyle = '#00aacc';
    ctx.fillRect(650, 80, 260, 60);
    ctx.fillStyle = '#883a00';
    ctx.fillRect(320, 360, 420, 50);

    const envTexture = new THREE.CanvasTexture(cv);
    envTexture.mapping = THREE.EquirectangularReflectionMapping;
    this.scene.environment = envTexture;
    this.envTexture = envTexture;

    // Lighting
    this.scene.add(new THREE.AmbientLight(0x061120, 1.4));

    const coreLight = new THREE.PointLight(0x00f0ff, 6.0, 10, 1.3);
    this.scene.add(coreLight);

    const fireLight = new THREE.PointLight(0xff6600, 4.5, 8, 1.5);
    this.scene.add(fireLight);

    const keyTop = new THREE.DirectionalLight(0xdcf5ff, 3.2);
    keyTop.position.set(5, 8, 5);
    this.scene.add(keyTop);

    const botRim = new THREE.DirectionalLight(0xff5500, 2.0);
    botRim.position.set(-5, -6, -5);
    this.scene.add(botRim);
  }

  buildCoreSingularity() {
    // White-Hot Arc Core
    this.singularityMesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.35, 32, 32),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    this.masterGroup.add(this.singularityMesh);

    // Cyan Electric Halo
    const haloMat = new THREE.ShaderMaterial({
      uniforms: { time: { value: 0 } },
      vertexShader: `
        varying vec3 vNorm;
        void main() {
          vNorm = normalize(normalMatrix * normal);
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        varying vec3 vNorm;
        uniform float time;
        void main() {
          float rim = pow(1.0 - abs(dot(vNorm, vec3(0.0, 0.0, 1.0))), 2.2);
          vec3 cyan = vec3(0.0, 0.9, 1.0) * rim * 3.8;
          gl_FragColor = vec4(cyan, rim);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide
    });
    this.haloMesh = new THREE.Mesh(new THREE.SphereGeometry(0.48, 32, 32), haloMat);
    this.masterGroup.add(this.haloMesh);

    // Large Faceted Obsidian Gem Core
    const obsidianMat = new THREE.MeshPhysicalMaterial({
      color: 0x020712,
      metalness: 0.25,
      roughness: 0.02,
      transmission: 0.60,
      opacity: 0.96,
      transparent: true,
      ior: 2.4,
      reflectivity: 1.0,
      clearcoat: 1.0,
      clearcoatRoughness: 0.01,
      envMap: this.envTexture,
      envMapIntensity: 4.2
    });

    this.obsidianCrystal = new THREE.Mesh(new THREE.IcosahedronGeometry(0.92, 1), obsidianMat);
    this.masterGroup.add(this.obsidianCrystal);

    this.crystalWire = new THREE.Mesh(
      new THREE.IcosahedronGeometry(0.924, 1),
      new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        wireframe: true,
        transparent: true,
        opacity: 0.35,
        blending: THREE.AdditiveBlending
      })
    );
    this.masterGroup.add(this.crystalWire);
  }

  buildPlasmaRings() {
    this.fireShaderMat = new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        colHot: { value: new THREE.Color(0xff4500) },
        colSun: { value: new THREE.Color(0xffaa00) }
      },
      vertexShader: `
        varying vec2 vUv;
        void main() {
          vUv = uv;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 colHot;
        uniform vec3 colSun;
        varying vec2 vUv;
        void main() {
          float flow = sin(vUv.x * 20.0 - time * 6.0) * 0.5 + 0.5;
          float heat = pow(flow, 2.0);
          vec3 c = mix(colHot, colSun, heat);
          c += vec3(0.8, 0.3, 0.0) * sin(vUv.x * 40.0 + time * 12.0);
          gl_FragColor = vec4(c * 2.8, 0.95);
        }
      `,
      transparent: true,
      blending: THREE.AdditiveBlending
    });

    this.fireRing = new THREE.Mesh(new THREE.TorusGeometry(1.25, 0.075, 32, 100), this.fireShaderMat);
    this.fireRing.rotation.x = Math.PI / 2.2;
    this.masterGroup.add(this.fireRing);
  }

  buildHeavyGimbals() {
    const titaniumMat = new THREE.MeshStandardMaterial({
      color: 0x8a99a8,
      metalness: 0.94,
      roughness: 0.25,
      envMap: this.envTexture,
      envMapIntensity: 2.6
    });

    const darkChassisMat = new THREE.MeshStandardMaterial({
      color: 0x181c22,
      metalness: 0.88,
      roughness: 0.38,
      envMap: this.envTexture,
      envMapIntensity: 1.5
    });

    const bronzeTrimMat = new THREE.MeshStandardMaterial({
      color: 0xcc7a29,
      metalness: 0.96,
      roughness: 0.18,
      envMap: this.envTexture,
      envMapIntensity: 3.0
    });

    const createChassis = (radius, width, thickness, segments, mainM, trimM) => {
      const g = new THREE.Group();

      const track = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, width, 80, 1, true), mainM);
      track.rotation.z = Math.PI / 2;
      g.add(track);

      const lip1 = new THREE.Mesh(new THREE.TorusGeometry(radius, thickness * 0.45, 16, 80), trimM);
      lip1.position.z = width / 2;
      g.add(lip1);

      const lip2 = lip1.clone();
      lip2.position.z = -width / 2;
      g.add(lip2);

      for (let i = 0; i < segments; i++) {
        const th = (i / segments) * Math.PI * 2;
        const clamp = new THREE.Group();

        const block = new THREE.Mesh(
          new THREE.BoxGeometry(thickness * 3.2, width * 1.26, thickness * 3.2),
          (i % 2 === 0) ? mainM : darkChassisMat
        );
        clamp.add(block);

        const bolt = new THREE.Mesh(
          new THREE.BoxGeometry(thickness * 3.8, width * 0.65, thickness * 1.8),
          bronzeTrimMat
        );
        clamp.add(bolt);

        const diode = new THREE.Mesh(
          new THREE.BoxGeometry(thickness * 0.9, width * 1.32, thickness * 1.1),
          new THREE.MeshBasicMaterial({ color: (i % 3 === 0) ? 0x00f0ff : 0xff8800 })
        );
        clamp.add(diode);

        clamp.position.set(Math.cos(th) * radius, Math.sin(th) * radius, 0);
        clamp.rotation.z = th + Math.PI / 2;
        g.add(clamp);
      }
      return g;
    };

    const inner = createChassis(1.75, 0.28, 0.08, 12, titaniumMat, bronzeTrimMat);
    const mid = createChassis(2.25, 0.38, 0.10, 16, darkChassisMat, titaniumMat);
    const outer = createChassis(2.80, 0.50, 0.12, 20, titaniumMat, darkChassisMat);

    this.scene.add(inner);
    this.scene.add(mid);
    this.scene.add(outer);

    this.gimbals = [inner, mid, outer];
  }

  buildParticles() {
    const count = 260;
    const pGeo = new THREE.BufferGeometry();
    const pPos = new Float32Array(count * 3);
    this.particleOrbits = [];

    for (let i = 0; i < count; i++) {
      const r = 0.8 + Math.random() * 2.2;
      const th = Math.random() * Math.PI * 2;
      pPos[i * 3] = Math.cos(th) * r;
      pPos[i * 3 + 1] = (Math.random() - 0.5) * 1.0;
      pPos[i * 3 + 2] = Math.sin(th) * r;
      this.particleOrbits.push({ r, th, s: 0.006 + Math.random() * 0.015 });
    }
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));

    const pMat = new THREE.PointsMaterial({
      color: 0x00f0ff, size: 0.042, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending
    });
    this.particles = new THREE.Points(pGeo, pMat);
    this.masterGroup.add(this.particles);
  }

  initPostProcessing() {
    const renderScene = new THREE.RenderPass(this.scene, this.camera);
    const bloomPass = new THREE.UnrealBloomPass(
      new THREE.Vector2(window.innerWidth, window.innerHeight),
      1.1, 0.45, 0.68
    );
    this.composer = new THREE.EffectComposer(this.renderer);
    this.composer.addPass(renderScene);
    this.composer.addPass(bloomPass);
  }

  initEvents() {
    window.addEventListener('mousemove', (e) => {
      this.mouseX = (e.clientX - window.innerWidth / 2) * 0.0003;
      this.mouseY = (e.clientY - window.innerHeight / 2) * 0.0003;
    });

    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
      this.composer.setSize(window.innerWidth, window.innerHeight);
    });
  }

  animate() {
    requestAnimationFrame(this.animate.bind(this));
    const dt = this.clock.getElapsedTime();

    // Parallax Interpolation
    this.targetX += (this.mouseX - this.targetX) * 0.05;
    this.targetY += (this.mouseY - this.targetY) * 0.05;
    this.scene.rotation.y = this.targetX * 1.15;
    this.scene.rotation.x = this.targetY * 1.15;

    // Obsidian Core Rotation
    if (this.obsidianCrystal) {
      this.obsidianCrystal.rotation.x += 0.003;
      this.obsidianCrystal.rotation.y += 0.005;
      this.crystalWire.rotation.x = this.obsidianCrystal.rotation.x;
      this.crystalWire.rotation.y = this.obsidianCrystal.rotation.y;
    }

    // Singularity Pulse
    const pulse = 1.0 + Math.sin(dt * 3.5) * 0.04;
    this.singularityMesh.scale.set(pulse, pulse, pulse);
    this.haloMesh.scale.set(pulse * 1.04, pulse * 1.04, pulse * 1.04);
    this.haloMesh.material.uniforms.time.value = dt;

    // Fire Plasma Swirl
    if (this.fireShaderMat) {
      this.fireShaderMat.uniforms.time.value = dt;
      this.fireRing.rotation.z += 0.012;
    }

    // Smooth Heavy Gyroscopic Velocities
    if (this.gimbals.length === 3) {
      this.gimbals[0].rotation.x = Math.sin(dt * 0.3) * 0.35;
      this.gimbals[0].rotation.y += 0.005;

      this.gimbals[1].rotation.x += 0.003;
      this.gimbals[1].rotation.y = Math.cos(dt * 0.25) * 0.45;

      this.gimbals[2].rotation.x = 0.28 + Math.sin(dt * 0.18) * 0.14;
      this.gimbals[2].rotation.y -= 0.002;
    }

    // Particle Swarm Physics
    if (this.particles) {
      const pArr = this.particles.geometry.attributes.position.array;
      for (let i = 0; i < this.particleOrbits.length; i++) {
        this.particleOrbits[i].th += this.particleOrbits[i].s;
        pArr[i * 3] = Math.cos(this.particleOrbits[i].th) * this.particleOrbits[i].r;
        pArr[i * 3 + 2] = Math.sin(this.particleOrbits[i].th) * this.particleOrbits[i].r;
      }
      this.particles.geometry.attributes.position.needsUpdate = true;
    }

    // Telemetry Jitter Dispatch
    if (Math.random() > 0.95) {
      const event = new CustomEvent('telemetry-update', {
        detail: {
          output: (8.40 + Math.random() * 0.18).toFixed(2) + " TW/s",
          temp: (4.80 + Math.random() * 0.1).toFixed(2) + " MK"
        }
      });
      window.dispatchEvent(event);
    }

    this.controls.update();
    this.composer.render();
  }
}

window.QuantumCoreEngine = QuantumCoreEngine;
