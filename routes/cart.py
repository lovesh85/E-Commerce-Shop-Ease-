from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from app import db, csrf
from models import Product, CartItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def view_cart():
    # Get all cart items for current user
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@cart_bp.route('/api/cart/add', methods=['POST'])
@login_required
@csrf.exempt
def add_to_cart():
    # Get data from request
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400
    
    # Check if product exists
    product = Product.query.get_or_404(product_id)
    
    # Check if product is in stock
    if product.stock < quantity:
        return jsonify({
            'success': False, 
            'message': f'Not enough stock. Only {product.stock} available.'
        }), 400
    
    # Check if item is already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # Update quantity if already in cart
        cart_item.quantity += quantity
        db.session.commit()
        message = 'Cart updated successfully!'
    else:
        # Add new item to cart
        new_cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(new_cart_item)
        db.session.commit()
        message = 'Item added to cart!'
    
    # Get updated cart count
    cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'success': True,
        'message': message,
        'cart_count': cart_count
    })

@cart_bp.route('/api/cart/update', methods=['POST'])
@login_required
@csrf.exempt
def update_cart():
    # Get data from request
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    quantity = int(data.get('quantity', 1))
    
    if not cart_item_id:
        return jsonify({'success': False, 'message': 'Cart item ID is required'}), 400
    
    # Get cart item
    cart_item = CartItem.query.filter_by(
        id=cart_item_id, 
        user_id=current_user.id
    ).first_or_404()
    
    # Check stock
    if quantity > cart_item.product.stock:
        return jsonify({
            'success': False,
            'message': f'Not enough stock. Only {cart_item.product.stock} available.'
        }), 400
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        db.session.delete(cart_item)
        message = 'Item removed from cart!'
    else:
        # Update quantity
        cart_item.quantity = quantity
        message = 'Cart updated!'
    
    db.session.commit()
    
    # Recalculate cart total
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return jsonify({
        'success': True,
        'message': message,
        'item_total': cart_item.product.price * quantity if quantity > 0 else 0,
        'cart_total': total
    })

@cart_bp.route('/api/cart/remove', methods=['POST'])
@login_required
@csrf.exempt
def remove_from_cart():
    # Get data from request
    data = request.get_json()
    cart_item_id = data.get('cart_item_id')
    
    if not cart_item_id:
        return jsonify({'success': False, 'message': 'Cart item ID is required'}), 400
    
    # Get cart item and delete
    cart_item = CartItem.query.filter_by(
        id=cart_item_id, 
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    # Recalculate cart total
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return jsonify({
        'success': True,
        'message': 'Item removed from cart!',
        'cart_total': total
    })

@cart_bp.route('/api/cart/count')
@login_required
@csrf.exempt
def get_cart_count():
    """Get the number of items in the cart"""
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})
