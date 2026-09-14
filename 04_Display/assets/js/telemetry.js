export class TelemetryMonitor {
    constructor() {
        this.cpuEl = document.getElementById('cpu-stat');
        this.ramEl = document.getElementById('ram-stat');
        this.lmDot = document.getElementById('lm-dot');
        this.lmText = document.getElementById('lm-status');
    }

    start(interval = 1600) {
        this.poll();
        setInterval(() => this.poll(), interval);
    }

    async poll() {
        try {
            const res = await fetch('/api/telemetry');
            const data = await res.json();
            if (this.cpuEl) this.cpuEl.innerText = `${data.cpu}%`;
            if (this.ramEl) this.ramEl.innerText = `${data.ram}%`;

            if (data.lm_online) {
                this.lmDot.className = "dot online";
                this.lmText.innerText = "QWEN 1.5B";
            } else {
                this.lmDot.className = "dot";
                this.lmText.innerText = "OFFLINE";
            }
        } catch (e) {}
    }
}
