// 1. Audio Frequency Visualizer
const scopeCanvas = document.getElementById('scope-canvas');
const scopeCtx = scopeCanvas.getContext('2d');
let scopePhase = 0;

function drawAudioScope() {
    scopeCtx.clearRect(0, 0, scopeCanvas.width, scopeCanvas.height);
    scopeCtx.beginPath();
    scopeCtx.strokeStyle = '#00f0ff';
    scopeCtx.lineWidth = 1.5;
    scopeCtx.shadowBlur = 6;
    scopeCtx.shadowColor = '#00f0ff';

    for (let i = 0; i < scopeCanvas.width; i++) {
        let v = Math.sin((i + scopePhase) * 0.08) * 8 + Math.cos((i - scopePhase) * 0.03) * 6 + scopeCanvas.height / 2;
        if (i === 0) scopeCtx.moveTo(i, v);
        else scopeCtx.lineTo(i, v);
    }
    scopeCtx.stroke();
    scopePhase += 1.8;
    requestAnimationFrame(drawAudioScope);
}
drawAudioScope();

// 2. Three.js Dual Setup (Stage 1 & Stage 2 Presence)
let scene1, camera1, renderer1, sphere1, wire1;
let scene2, camera2, renderer2, sphere2, wire2;

function initSphere1() {
    const el = document.getElementById('stage1-sphere-container');
    scene1 = new THREE.Scene();
    camera1 = new THREE.PerspectiveCamera(45, el.clientWidth / el.clientHeight, 0.1, 1000);
    camera1.position.z = 240;

    renderer1 = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer1.setSize(el.clientWidth, el.clientHeight);
    el.appendChild(renderer1.domElement);

    const geo = new THREE.IcosahedronGeometry(70, 3);
    const mat = new THREE.PointsMaterial({ color: 0x00f0ff, size: 2.2, transparent: true, opacity: 0.85 });
    sphere1 = new THREE.Points(geo, mat);
    scene1.add(sphere1);

    const wireMat = new THREE.MeshBasicMaterial({ color: 0x0066ff, wireframe: true, transparent: true, opacity: 0.3 });
    wire1 = new THREE.Mesh(new THREE.IcosahedronGeometry(52, 1), wireMat);
    scene1.add(wire1);
}

function initSphere2() {
    const el = document.getElementById('presence-sphere-container');
    scene2 = new THREE.Scene();
    camera2 = new THREE.PerspectiveCamera(45, el.clientWidth / el.clientHeight, 0.1, 1000);
    camera2.position.z = 260;

    renderer2 = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer2.setSize(el.clientWidth, el.clientHeight);
    el.appendChild(renderer2.domElement);

    const geo = new THREE.IcosahedronGeometry(85, 4);
    const mat = new THREE.PointsMaterial({ color: 0x00f0ff, size: 2.5, transparent: true, opacity: 0.9 });
    sphere2 = new THREE.Points(geo, mat);
    scene2.add(sphere2);

    const wireMat = new THREE.MeshBasicMaterial({ color: 0x00ffaa, wireframe: true, transparent: true, opacity: 0.25 });
    wire2 = new THREE.Mesh(new THREE.IcosahedronGeometry(62, 2), wireMat);
    scene2.add(wire2);
}

function animateSpheres() {
    requestAnimationFrame(animateSpheres);
    if (sphere1) {
        sphere1.rotation.y += 0.005;
        wire1.rotation.y -= 0.007;
        renderer1.render(scene1, camera1);
    }
    if (sphere2) {
        sphere2.rotation.y += 0.008;
        sphere2.rotation.x += 0.003;
        wire2.rotation.y -= 0.01;
        renderer2.render(scene2, camera2);
    }
}

window.addEventListener('load', () => {
    initSphere1();
    initSphere2();
    animateSpheres();
});

// 3. Stage Transitions
function activateNeuralLink() {
    document.getElementById('stage-dashboard').classList.remove('active');
    document.getElementById('stage-presence').classList.add('active');
    
    // Voice prompt trigger
    speakTTS("Neural link active. I am Ultron. What is your directive, Director?");
}

function deactivateNeuralLink() {
    document.getElementById('stage-presence').classList.remove('active');
    document.getElementById('stage-dashboard').classList.add('active');
}

// 4. Voice vs Chat Mode Toggle
let commsMode = 'voice';
function switchCommsMode(mode) {
    commsMode = mode;
    const vBtn = document.getElementById('mode-voice-btn');
    const cBtn = document.getElementById('mode-chat-btn');
    const chatDeck = document.getElementById('chat-deck');
    const vHud = document.getElementById('voice-state-indicator');

    if (mode === 'voice') {
        vBtn.classList.add('active');
        cBtn.classList.remove('active');
        chatDeck.classList.add('hidden');
        vHud.style.display = 'flex';
    } else {
        cBtn.classList.add('active');
        vBtn.classList.remove('active');
        chatDeck.classList.remove('hidden');
        vHud.style.display = 'none';
    }
}

// 5. Native Browser Speech Synthesis (Zero Latency Ultron Voice)
function speakTTS(text) {
    if (!window.speechSynthesis) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 0.85; // Deeper futuristic tone
    window.speechSynthesis.speak(utterance);
}

// 6. Chat Directive Transmission
async function sendChatMessage() {
    const input = document.getElementById('presence-input');
    const txt = input.value.trim();
    if (!txt) return;
    input.value = "";

    appendChatMessage("YOU: " + txt, "user");

    try {
        const res = await fetch('/api/command', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ command: txt })
        });
        const d = await res.json();
        appendChatMessage(`[${d.agent}]: ${d.reply}`, "ai");
        if (commsMode === 'voice') speakTTS(d.reply);
    } catch(e) {
        appendChatMessage("[ERROR]: Neural signal dropped.", "sys");
    }
}

function appendChatMessage(msg, cls) {
    const box = document.getElementById('presence-chat-logs');
    const line = document.createElement('div');
    line.className = `chat-line ${cls}`;
    line.innerText = msg;
    box.appendChild(line);
    box.scrollTop = box.scrollHeight;
}

// Telemetry Poller
async function syncTelemetry() {
    try {
        const res = await fetch('/api/telemetry');
        const data = await res.json();
        document.getElementById('cpu-metric').innerText = `${data.cpu}%`;
        document.getElementById('ram-metric').innerText = `${data.ram}%`;

        const pill = document.getElementById('lm-pill');
        if (data.lm_online) {
            pill.className = "gauge-val";
            pill.innerText = "QWEN 1.5B";
            pill.style.color = "#00ff88";
        } else {
            pill.className = "gauge-val blink-warn";
            pill.innerText = "OFFLINE";
            pill.style.color = "#ff0055";
        }
    } catch(e) {}
}
setInterval(syncTelemetry, 1500);
