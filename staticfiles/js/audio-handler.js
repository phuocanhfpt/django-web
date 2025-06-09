// Audio handler with proper error handling
class AudioHandler {
    constructor() {
        this.audioContext = null;
        this.audioBuffers = new Map();
        this.initializeAudioContext();
    }

    async initializeAudioContext() {
        try {
            // Create audio context
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            this.audioContext = new AudioContext();

            // Preload audio files
            await this.preloadAudio('notification', '/static/audio/notification.mp3');
            await this.preloadAudio('fallback', '/static/audio/fallback-notification.mp3');
        } catch (error) {
            console.warn('Audio context initialization failed:', error);
        }
    }

    async preloadAudio(name, url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const arrayBuffer = await response.arrayBuffer();
            const audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
            this.audioBuffers.set(name, audioBuffer);
        } catch (error) {
            console.warn(`Failed to preload audio ${name}:`, error);
        }
    }

    async playSound(name) {
        try {
            if (!this.audioContext) {
                await this.initializeAudioContext();
            }

            const buffer = this.audioBuffers.get(name);
            if (!buffer) {
                console.warn(`Audio buffer ${name} not found`);
                return;
            }

            const source = this.audioContext.createBufferSource();
            source.buffer = buffer;
            source.connect(this.audioContext.destination);
            source.start(0);
        } catch (error) {
            console.warn(`Failed to play sound ${name}:`, error);
        }
    }
}

// Initialize audio handler
const audioHandler = new AudioHandler();

// Export for use in other files
window.audioHandler = audioHandler; 