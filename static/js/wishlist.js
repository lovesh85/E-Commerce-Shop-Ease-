// Wishlist functionality for ShopEase

document.addEventListener('DOMContentLoaded', function() {
    // Toggle wishlist buttons
    const wishlistToggleButtons = document.querySelectorAll('.toggle-wishlist');
    wishlistToggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productId = this.dataset.productId;
            toggleWishlist(productId, this);
        });
    });
    
    // Remove from wishlist buttons
    const removeButtons = document.querySelectorAll('.remove-from-wishlist');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const wishlistItemId = this.dataset.wishlistItemId;
            
            removeFromWishlist(wishlistItemId);
        });
    });
});

// Toggle product in wishlist
function toggleWishlist(productId, buttonElement) {
    showLoading();
    
    fetch('/api/wishlist/toggle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Update button state
            if (buttonElement) {
                if (data.action === 'added') {
                    buttonElement.classList.add('active');
                    buttonElement.setAttribute('title', 'Remove from Wishlist');
                } else {
                    buttonElement.classList.remove('active');
                    buttonElement.setAttribute('title', 'Add to Wishlist');
                }
            }
            
            updateWishlistCount();
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error toggling wishlist:', error);
        showToast('An error occurred. Please try again.', 'danger');
    });
}

// Remove item from wishlist
function removeFromWishlist(wishlistItemId) {
    showLoading();
    
    fetch('/api/wishlist/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            wishlist_item_id: wishlistItemId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Remove card from wishlist
            const wishlistItem = document.querySelector(`#wishlist-item-${wishlistItemId}`);
            if (wishlistItem) {
                wishlistItem.remove();
            }
            
            // If wishlist is empty, show empty message
            const wishlistContainer = document.querySelector('#wishlist-container');
            if (wishlistContainer && wishlistContainer.querySelectorAll('.wishlist-item').length === 0) {
                wishlistContainer.innerHTML = `
                    <div class="text-center py-5">
                        <h3>Your wishlist is empty</h3>
                        <p>Add products to your wishlist</p>
                        <a href="/products" class="btn btn-primary">Browse Products</a>
                    </div>
                `;
            }
            
            updateWishlistCount();
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error removing from wishlist:', error);
        showToast('An error occurred. Please try again.', 'danger');
    });
}
