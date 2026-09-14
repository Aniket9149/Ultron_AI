// 1. Live Dynamic Clock
function updateClock() {
    const now = new Date();
    const hrs = String(now.getHours()).padStart(2, '0');
    const mins = String(now.getMinutes()).padStart(2, '0');
    const secs = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('hud-time').innerText = `${hrs}:${mins}:${secs}`;
    
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    document.getElementById('hud-date').innerText = `${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}`;
    document.getElementById('hud-day').innerText = days[now.getDay()];
}
setInterval(updateClock, 1000);
updateClock();

// 2. Real-Time Waveforms
const nCanvas = document.getElementById('neural-canvas');
const nCtx = nCanvas.getContext('2d');
let nStep = 0;
function drawNeuralWave() {
    nCtx.clearRect(0, 0, nCanvas.width, nCanvas.height);
    nCtx.beginPath();
    nCtx.strokeStyle = '#00f0ff';
    nCtx.lineWidth = 1.6;
    for (let x = 0; x < nCanvas.width; x++) {
        let y = Math.sin((x + nStep) * 0.14) * (Math.sin(x * 0.05) * 11) + nCanvas.height / 2;
        if (x === 0) nCtx.moveTo(x, y);
        else nCtx.lineTo(x, y);
    }
    nCtx.stroke();
    nStep += 2.5;
    requestAnimationFrame(drawNeuralWave);
}
drawNeuralWave();

const mCanvas = document.getElementById('mini-core-wave');
const mCtx = mCanvas.getContext('2d');
let mStep = 0;
function drawMiniWave() {
    mCtx.clearRect(0, 0, mCanvas.width, mCanvas.height);
    mCtx.beginPath();
    mCtx.strokeStyle = '#38bdf8';
    mCtx.lineWidth = 1.2;
    for (let x = 0; x < mCanvas.width; x++) {
        let y = Math.sin((x + mStep) * 0.16) * 5 + mCanvas.height / 2;
        if (x === 0) mCtx.moveTo(x, y);
        else mCtx.lineTo(x, y);
    }
    mCtx.stroke();
    mStep += 1.8;
    requestAnimationFrame(drawMiniWave);
}
drawMiniWave();

// 3. Three.js Rotating Holographic Core
const coreContainer = document.getElementById('spatial-core-anchor');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(40, coreContainer.clientWidth / coreContainer.clientHeight, 0.1, 1000);
camera.position.z = 210;

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(coreContainer.clientWidth, coreContainer.clientHeight);
coreContainer.appendChild(renderer.domElement);

// Octahedron Core Mesh with Cyan Hologram Glow
const geo = new THREE.OctahedronGeometry(42, 0);
const wireMat = new THREE.MeshBasicMaterial({ color: 0x00f0ff, wireframe: true, transparent: true, opacity: 0.75 });
const wireMesh = new THREE.Mesh(geo, wireMat);
scene.add(wireMesh);

const innerGeo = new THREE.OctahedronGeometry(26, 0);
const innerMat = new THREE.MeshBasicMaterial({ color: 0x0088cc, wireframe: true, transparent: true, opacity: 0.4 });
const innerMesh = new THREE.Mesh(innerGeo, innerMat);
scene.add(innerMesh);

function animate3D() {
    requestAnimationFrame(animate3D);
    wireMesh.rotation.y += 0.007;
    wireMesh.rotation.x += 0.003;
    innerMesh.rotation.y -= 0.01;
    renderer.render(scene, camera);
}
animate3D();

// 4. Live Telemetry Poller
async function updateVitals() {
    try {
        const res = await fetch('/api/telemetry');
        const data = await res.json();
        document.getElementById('val-cpu').innerText = `${Math.round(data.cpu)}%`;
        document.getElementById('val-mem').innerText = `${Math.round(data.ram)}%`;
    } catch(e) {}
}
setInterval(updateVitals, 2000);

// 5. Interaction & Voice Hook
function selectTab(name) {
    speakText(`${name} subsystem engaged.`);
}

function triggerCorePresence() {
    const banner = document.getElementById('voice-banner');
    banner.classList.add('active');
    speakText("Ultron online. I am listening, Director.");
    setTimeout(() => banner.classList.remove('active'), 3500);
}

function speakText(txt) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(txt);
    utt.rate = 1.0;
    utt.pitch = 0.85;
    window.speechSynthesis.speak(utt);
}
