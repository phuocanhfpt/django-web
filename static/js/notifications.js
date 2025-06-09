// Notification handler with proper error handling
class NotificationHandler {
    constructor() {
        this.audioElement = null;
        this.notificationSound = null;
        this.userInteracted = false;
        this.audioLoaded = false;
        this.initializeAudio();
        this.setupUserInteraction();
    }

    setupUserInteraction() {
        // Listen for any user interaction
        const events = ['click', 'touchstart', 'keydown'];
        events.forEach(event => {
            document.addEventListener(event, () => {
                this.userInteracted = true;
                // Try to initialize audio after user interaction
                if (!this.audioLoaded) {
                    this.initializeAudio();
                }
            }, { once: true });
        });
    }

    initializeAudio() {
        try {
            // Create audio element
            this.audioElement = new Audio();
            
            // Try to load notification sound with fallback
            const notificationPath = '/static/audio/notification.mp3';
            const fallbackPath = '/static/audio/fallback-notification.mp3';
            
            this.audioElement.addEventListener('error', (e) => {
                console.warn('Failed to load primary notification sound, trying fallback...');
                this.audioElement.src = fallbackPath;
            });

            this.audioElement.addEventListener('canplaythrough', () => {
                this.audioLoaded = true;
                console.log('Audio loaded successfully');
            });

            this.audioElement.src = notificationPath;
            
            // Preload audio
            this.audioElement.load();
        } catch (error) {
            console.warn('Audio initialization failed:', error);
        }
    }

    async playNotification() {
        try {
            if (!this.userInteracted) {
                console.warn('Waiting for user interaction before playing audio');
                return;
            }

            if (!this.audioLoaded) {
                console.warn('Audio not loaded yet');
                return;
            }

            if (this.audioElement) {
                // Reset audio to start
                this.audioElement.currentTime = 0;
                
                // Play with user interaction
                const playPromise = this.audioElement.play();
                
                if (playPromise !== undefined) {
                    playPromise.catch(error => {
                        console.warn('Audio play failed:', error);
                    });
                }
            }
        } catch (error) {
            console.warn('Failed to play notification:', error);
        }
    }

    // Handle notification display
    showNotification(title, options = {}) {
        try {
            if (!("Notification" in window)) {
                console.warn("This browser does not support desktop notifications");
                return;
            }

            if (Notification.permission === "granted") {
                new Notification(title, options);
            } else if (Notification.permission !== "denied") {
                Notification.requestPermission().then(permission => {
                    if (permission === "granted") {
                        new Notification(title, options);
                    }
                });
            }
        } catch (error) {
            console.warn('Failed to show notification:', error);
        }
    }
}

// Initialize notification handler
const notificationHandler = new NotificationHandler();

// Export for use in other files
window.notificationHandler = notificationHandler; 