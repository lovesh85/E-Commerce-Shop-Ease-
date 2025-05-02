// Main JavaScript file for ShopEase eCommerce site

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize any flash messages
    const flashMessages = document.querySelectorAll('.alert-dismissible');
    flashMessages.forEach((flash) => {
        // Auto-dismiss flash messages after 5 seconds
        setTimeout(() => {
            const alert = new bootstrap.Alert(flash);
            alert.close();
        }, 5000);
    });
    
    // Update cart and wishlist counts if user is logged in
    if (document.querySelector('#cart-count') || document.querySelector('#wishlist-count')) {
        updateCartCount();
        updateWishlistCount();
    }
    
    // Search form functionality
    const searchForm = document.querySelector('#search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = document.querySelector('#search-input');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                return false;
            }
        });
    }
    
    // Back button functionality
    const backButtons = document.querySelectorAll('.btn-back');
    backButtons.forEach(button => {
        button.addEventListener('click', function() {
            history.back();
        });
    });
    
    // Theme toggle is now handled in theme-toggle.js
});

// Function to update cart count
function updateCartCount() {
    const cartCountElement = document.querySelector('#cart-count');
    if (!cartCountElement) return;
    
    fetch('/api/cart/count', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            cartCountElement.textContent = data.count;
            if (data.count > 0) {
                cartCountElement.classList.remove('d-none');
            } else {
                cartCountElement.classList.add('d-none');
            }
        })
        .catch(error => console.error('Error fetching cart count:', error));
}

// Function to update wishlist count
function updateWishlistCount() {
    const wishlistCountElement = document.querySelector('#wishlist-count');
    if (!wishlistCountElement) return;
    
    fetch('/api/wishlist/count', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            wishlistCountElement.textContent = data.count;
            if (data.count > 0) {
                wishlistCountElement.classList.remove('d-none');
            } else {
                wishlistCountElement.classList.add('d-none');
            }
        })
        .catch(error => console.error('Error fetching wishlist count:', error));
}

// Show toast message
function showToast(message, type = 'success') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // Create toast container if it doesn't exist
        const newToastContainer = document.createElement('div');
        newToastContainer.id = 'toast-container';
        newToastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(newToastContainer);
        
        // Update reference
        toastContainer = newToastContainer;
    }
    
    // Create toast element
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-bg-${type} border-0`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Toast content
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Add toast to container
    toastContainer.appendChild(toastEl);
    
    // Initialize Bootstrap toast
    const toast = new bootstrap.Toast(toastEl, {
        autohide: true,
        delay: 3000
    });
    
    // Show toast
    toast.show();
    
    // Remove toast element after it's hidden
    toastEl.addEventListener('hidden.bs.toast', function() {
        toastEl.remove();
    });
}

// Format price to display as currency in Indian Rupees
function formatCurrency(price) {
    // Convert USD to INR (1 USD = 75 INR approximately)
    const priceInRupees = price * 75;
    
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0 // No decimal points for rupees
    }).format(priceInRupees);
}

// Get CSRF token for AJAX requests
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Add/Remove loading spinner
function showLoading() {
    // Create spinner overlay if it doesn't exist
    let spinnerOverlay = document.getElementById('spinner-overlay');
    if (!spinnerOverlay) {
        spinnerOverlay = document.createElement('div');
        spinnerOverlay.id = 'spinner-overlay';
        spinnerOverlay.className = 'spinner-overlay';
        spinnerOverlay.innerHTML = `
            <div class="spinner-border text-light" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        document.body.appendChild(spinnerOverlay);
    }
    spinnerOverlay.style.display = 'flex';
}

function hideLoading() {
    const spinnerOverlay = document.getElementById('spinner-overlay');
    if (spinnerOverlay) {
        spinnerOverlay.style.display = 'none';
    }
}
