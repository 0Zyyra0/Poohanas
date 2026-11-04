/**
 * Poohanas - Main JavaScript
 * Premium Graphics Card E-Commerce
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize mobile menu
    initMobileMenu();

    // Initialize alerts/dismissible messages
    initAlerts();

    // Initialize quantity controls
    initQuantityControls();

    // Initialize form validation
    initFormValidation();

    // Initialize wishlist buttons
    initWishlistButtons();

    // Initialize cart actions
    initCartActions();
});

/**
 * Mobile menu toggle
 */
function initMobileMenu() {
    const menuBtn = document.querySelector('.mobile-menu-btn');
    const navMain = document.querySelector('.nav-main');

    if (menuBtn && navMain) {
        menuBtn.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            navMain.classList.toggle('active');
            menuBtn.classList.toggle('active');
        });
    }
}

/**
 * Alert/dismissible message handling
 */
function initAlerts() {
    document.querySelectorAll('.alert-close').forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        });

        // Auto-dismiss after 5 seconds
        const alert = button.closest('.alert');
        if (alert) {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        }
    });
}

/**
 * Quantity input controls
 */
function initQuantityControls() {
    document.querySelectorAll('.quantity-control').forEach(control => {
        const input = control.querySelector('.quantity-input');
        const minusBtn = control.querySelector('.quantity-btn.minus');
        const plusBtn = control.querySelector('.quantity-btn.plus');

        if (minusBtn && input) {
            minusBtn.addEventListener('click', function() {
                const min = parseInt(input.min) || 1;
                const value = parseInt(input.value) || min;
                if (value > min) {
                    input.value = value - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }

        if (plusBtn && input) {
            plusBtn.addEventListener('click', function() {
                const max = parseInt(input.max) || 99;
                const value = parseInt(input.value) || 1;
                if (value < max) {
                    input.value = value + 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}

/**
 * Form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
}

/**
 * Wishlist buttons
 */
function initWishlistButtons() {
    document.querySelectorAll('.wishlist-btn').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const isActive = this.classList.contains('active');
            const url = isActive
                ? `/wishlist/remove/${productId}/`
                : `/wishlist/add/${productId}/`;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                if (response.ok) {
                    if (isActive) {
                        this.classList.remove('active');
                        showToast('Removed from wishlist', 'success');
                    } else {
                        this.classList.add('active');
                        showToast('Added to wishlist', 'success');
                    }
                    // Reload to update count
                    setTimeout(() => location.reload(), 500);
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('Please log in to use wishlist', 'error');
            }
        });
    });
}

/**
 * Cart actions
 */
function initCartActions() {
    // Quick add to cart buttons
    document.querySelectorAll('.quick-add-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('button');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="spinner"></span>';
            }
        });
    });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Search form enhancement
 */
const searchForms = document.querySelectorAll('.search-form');
searchForms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const input = this.querySelector('.search-input');
        if (input && !input.value.trim()) {
            e.preventDefault();
        }
    });
});

/**
 * Image lazy loading
 */
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

/**
 * Reduced motion preference
 */
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (prefersReducedMotion.matches) {
    document.documentElement.style.setProperty('--transition-fast', '0ms');
    document.documentElement.style.setProperty('--transition-normal', '0ms');
    document.documentElement.style.setProperty('--transition-slow', '0ms');
}