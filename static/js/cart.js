// Cart functionality for ShopEase

document.addEventListener('DOMContentLoaded', function() {
    // Add to cart buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productId = this.dataset.productId;
            const quantityInput = document.querySelector('#quantity');
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
            
            addToCart(productId, quantity);
        });
    });
    
    // Update quantity buttons
    const quantityInputs = document.querySelectorAll('.cart-quantity');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const cartItemId = this.dataset.cartItemId;
            const newQuantity = parseInt(this.value);
            
            if (newQuantity <= 0) {
                // Ask for confirmation before removing
                if (confirm('Remove this item from cart?')) {
                    removeFromCart(cartItemId);
                } else {
                    // Reset to previous value if user cancels
                    this.value = 1;
                }
            } else {
                updateCartItem(cartItemId, newQuantity);
            }
        });
    });
    
    // Remove from cart buttons
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    removeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const cartItemId = this.dataset.cartItemId;
            
            if (confirm('Remove this item from cart?')) {
                removeFromCart(cartItemId);
            }
        });
    });
    
    // Quantity increment/decrement buttons
    document.querySelectorAll('.btn-quantity-change').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.closest('.input-group').querySelector('input');
            const currentValue = parseInt(input.value);
            
            if (this.dataset.action === 'increase') {
                input.value = currentValue + 1;
            } else if (this.dataset.action === 'decrease' && currentValue > 1) {
                input.value = currentValue - 1;
            }
            
            // Trigger change event for cart items
            if (input.classList.contains('cart-quantity')) {
                input.dispatchEvent(new Event('change'));
            }
        });
    });
});

// Add product to cart
function addToCart(productId, quantity = 1) {
    showLoading();
    
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            showToast(data.message, 'success');
            updateCartCount();
            
            // Update UI if on product detail page
            const addToCartBtn = document.querySelector('.add-to-cart');
            if (addToCartBtn) {
                addToCartBtn.textContent = 'Add More to Cart';
            }
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error adding to cart:', error);
        showToast('An error occurred. Please try again.', 'danger');
    });
}

// Update cart item quantity
function updateCartItem(cartItemId, quantity) {
    showLoading();
    
    fetch('/api/cart/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            cart_item_id: cartItemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Update item price display
            const itemTotalElement = document.querySelector(`#item-total-${cartItemId}`);
            if (itemTotalElement) {
                itemTotalElement.textContent = formatCurrency(data.item_total);
            }
            
            // Update cart total
            const cartTotalElement = document.querySelector('#cart-total');
            if (cartTotalElement) {
                cartTotalElement.textContent = formatCurrency(data.cart_total);
            }
            
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error updating cart:', error);
        showToast('An error occurred. Please try again.', 'danger');
    });
}

// Remove item from cart
function removeFromCart(cartItemId) {
    showLoading();
    
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            cart_item_id: cartItemId
        })
    })
    .then(response => response.json())
    .then(data => {
        hideLoading();
        
        if (data.success) {
            // Remove row from cart table
            const cartRow = document.querySelector(`#cart-item-${cartItemId}`);
            if (cartRow) {
                cartRow.remove();
            }
            
            // Update cart total
            const cartTotalElement = document.querySelector('#cart-total');
            if (cartTotalElement) {
                cartTotalElement.textContent = formatCurrency(data.cart_total);
            }
            
            // If cart is empty, show empty message
            const cartTable = document.querySelector('#cart-table');
            if (cartTable && cartTable.querySelectorAll('tbody tr').length === 0) {
                const cartContainer = document.querySelector('#cart-container');
                cartContainer.innerHTML = `
                    <div class="text-center py-5">
                        <h3>Your cart is empty</h3>
                        <p>Add some products to your cart</p>
                        <a href="/products" class="btn btn-primary">Continue Shopping</a>
                    </div>
                `;
            }
            
            updateCartCount();
            showToast(data.message, 'success');
        } else {
            showToast(data.message, 'danger');
        }
    })
    .catch(error => {
        hideLoading();
        console.error('Error removing from cart:', error);
        showToast('An error occurred. Please try again.', 'danger');
    });
}
