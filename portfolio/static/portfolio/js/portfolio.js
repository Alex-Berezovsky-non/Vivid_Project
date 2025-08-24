// Portfolio Gallery functionality
class PortfolioGallery {
    constructor() {
        this.grid = document.getElementById('portfolio-grid');
        this.items = document.querySelectorAll('.portfolio-item');
        this.photoItems = document.querySelectorAll('.photo-item');
        this.init();
    }

    init() {
        this.initializeLazyLoad();
        this.initializeAnimations();
        this.initializeFilters();
        this.initializeLightbox();
    }

    initializeLazyLoad() {
        if ('IntersectionObserver' in window) {
            const lazyObserver = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        lazyObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach((img) => {
                lazyObserver.observe(img);
            });
        }
    }

    initializeAnimations() {
        if (this.items.length > 0) {
            this.animateItems(this.items);
        }

        if (this.photoItems.length > 0) {
            this.animateItems(this.photoItems);
        }
    }

    animateItems(items) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, index * 100);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        items.forEach(item => {
            observer.observe(item);
        });
    }

    initializeFilters() {
        const filterForm = document.querySelector('.filter-form');
        if (filterForm) {
            filterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.applyFilters();
            });

            // Auto-submit on select change
            const selectElements = filterForm.querySelectorAll('select');
            selectElements.forEach(select => {
                select.addEventListener('change', () => this.applyFilters());
            });
        }
    }

    applyFilters() {
        const form = document.querySelector('.filter-form');
        const formData = new FormData(form);
        const params = new URLSearchParams();

        for (let [key, value] of formData) {
            if (value) params.append(key, value);
        }

        // Show loading state
        this.showLoading();

        fetch(`${window.location.pathname}?${params}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.getElementById('portfolio-grid');
            
            if (newContent) {
                this.grid.innerHTML = newContent.innerHTML;
                this.items = document.querySelectorAll('.portfolio-item');
                this.initializeAnimations();
            }
        })
        .catch(error => {
            console.error('Error:', error);
        })
        .finally(() => {
            this.hideLoading();
        });
    }

    showLoading() {
        // Create loading overlay if it doesn't exist
        let loadingOverlay = document.getElementById('loading-overlay');
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'loading-overlay';
            loadingOverlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            `;
            
            const spinner = document.createElement('div');
            spinner.className = 'loading-spinner';
            loadingOverlay.appendChild(spinner);
            
            document.body.appendChild(loadingOverlay);
        }
        
        loadingOverlay.style.display = 'flex';
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }

    initializeLightbox() {
        // This would be implemented based on your preferred lightbox library
        // For example, using PhotoSwipe, Lightbox2, or similar
        console.log('Lightbox initialization would go here');
    }

    openFullscreen(photoId) {
        const url = `/portfolio/media/${photoId}/fullscreen/`;
        window.open(url, '_blank', 'width=1200,height=800,scrollbars=no');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new PortfolioGallery();
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}