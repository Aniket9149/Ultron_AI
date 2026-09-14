export class VoiceEngine {
    constructor() {
        this.synth = window.speechSynthesis;
    }

    speak(text) {
        if (!this.synth) return;
        this.synth.cancel();
        const utt = new SpeechSynthesisUtterance(text);
        utt.rate = 1.0;
        utt.pitch = 0.9;
        this.synth.speak(utt);
    }
}
