export class ChatEngine {
    constructor(onReplyCallback) {
        this.streamBox = document.getElementById('chat-stream-box');
        this.input = document.getElementById('chat-prompt-input');
        this.onReply = onReplyCallback;
        this.bindEvents();
    }

    bindEvents() {
        if (this.input) {
            this.input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.send();
            });
        }
    }

    append(text, type) {
        const div = document.createElement('div');
        div.className = `msg ${type}`;
        div.innerText = text;
        this.streamBox.appendChild(div);
        this.streamBox.scrollTop = this.streamBox.scrollHeight;
    }

    async send() {
        const text = this.input.value.trim();
        if (!text) return;
        this.input.value = "";

        this.append(text, 'user');

        try {
            const res = await fetch('/api/command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command: text })
            });
            const d = await res.json();
            this.append(d.reply, 'ai');
            if (this.onReply) this.onReply(d.reply);
        } catch (e) {
            this.append("Bridge communication offline.", 'ai');
        }
    }
}
