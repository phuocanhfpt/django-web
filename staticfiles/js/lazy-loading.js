// Lazy loading handler with proper error handling
class LazyLoadingHandler {
    constructor() {
        this.placeholderImage = '/static/images/placeholder.svg';
        this.initializeLazyLoading();
    }

    initializeLazyLoading() {
        try {
            // Check if browser supports IntersectionObserver
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            this.loadImage(img);
                            observer.unobserve(img);
                        }
                    });
                });

                // Observe all lazy images
                document.querySelectorAll('img[data-src]').forEach(img => {
                    imageObserver.observe(img);
                });
            } else {
                // Fallback for browsers that don't support IntersectionObserver
                this.loadAllImages();
            }
        } catch (error) {
            console.warn('Lazy loading initialization failed:', error);
            this.loadAllImages();
        }
    }

    loadImage(img) {
        try {
            const src = img.getAttribute('data-src');
            if (!src) return;

            // Set placeholder while loading
            img.src = this.placeholderImage;

            // Create new image to test loading
            const tempImage = new Image();
            tempImage.onload = () => {
                img.src = src;
                img.classList.add('loaded');
            };
            tempImage.onerror = () => {
                console.warn('Failed to load image:', src);
                img.classList.add('load-error');
            };
            tempImage.src = src;
        } catch (error) {
            console.warn('Failed to load image:', error);
            img.classList.add('load-error');
        }
    }

    loadAllImages() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', () => {
    window.lazyLoadingHandler = new LazyLoadingHandler();
}); 