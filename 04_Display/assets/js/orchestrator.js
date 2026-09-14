import { SpatialCore3D } from './core_3d.js';
import { TelemetryMonitor } from './telemetry.js';
import { VoiceEngine } from './voice_engine.js';
import { ChatEngine } from './chat_engine.js';

class UIOrchestrator {
    constructor() {
        this.activeMode = 'voice';
        this.voice = new VoiceEngine();
        this.telemetry = new TelemetryMonitor();
        this.chat = new ChatEngine((reply) => {
            if (this.activeMode === 'voice') this.voice.speak(reply);
        });

        this.init();
    }

    init() {
        this.telemetry.start();
        this.init3D();
        this.bindUI();
    }

    init3D() {
        this.coreHub = new SpatialCore3D('spatial-canvas-hub', { radius: 65, detail: 2, speed: 0.003 });
        this.corePresence = new SpatialCore3D('spatial-canvas-presence', { radius: 75, detail: 3, speed: 0.005 });

        const loop = () => {
            requestAnimationFrame(loop);
            this.coreHub.tick();
            this.corePresence.tick();
        };
        loop();
    }

    bindUI() {
        document.getElementById('btn-init-presence').onclick = () => this.openPresence();
        document.getElementById('btn-back-hub').onclick = () => this.closePresence();
        document.getElementById('tab-voice').onclick = () => this.setMode('voice');
        document.getElementById('tab-chat').onclick = () => this.setMode('chat');
        document.getElementById('btn-send-chat').onclick = () => this.chat.send();
    }

    openPresence() {
        document.getElementById('stage-hub').classList.remove('active');
        document.getElementById('stage-presence').classList.add('active');
        this.voice.speak("Neural presence initialized. Ultron is listening.");
    }

    closePresence() {
        document.getElementById('stage-presence').classList.remove('active');
        document.getElementById('stage-hub').classList.add('active');
    }

    setMode(mode) {
        this.activeMode = mode;
        const tabV = document.getElementById('tab-voice');
        const tabC = document.getElementById('tab-chat');
        const vDeck = document.getElementById('voice-hud');
        const cModal = document.getElementById('chat-modal');

        if (mode === 'voice') {
            tabV.classList.add('active');
            tabC.classList.remove('active');
            vDeck.style.display = 'flex';
            cModal.classList.add('hidden');
        } else {
            tabC.classList.add('active');
            tabV.classList.remove('active');
            vDeck.style.display = 'none';
            cModal.classList.remove('hidden');
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    window.orchestrator = new UIOrchestrator();
});
