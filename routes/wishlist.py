from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_required, current_user
from app import db, csrf
from models import Product, WishlistItem

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist')
@login_required
def view_wishlist():
    # Get all wishlist items for current user
    wishlist_items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    
    return render_template('wishlist.html', wishlist_items=wishlist_items)

@wishlist_bp.route('/api/wishlist/add', methods=['POST'])
@login_required
@csrf.exempt
def add_to_wishlist():
    # Get data from request
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400
    
    # Check if product exists
    product = Product.query.get_or_404(product_id)
    
    # Check if item is already in wishlist
    wishlist_item = WishlistItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if wishlist_item:
        # Item already in wishlist
        return jsonify({
            'success': False,
            'message': 'Item already in wishlist!'
        })
    
    # Add new item to wishlist
    new_wishlist_item = WishlistItem(
        user_id=current_user.id,
        product_id=product_id
    )
    db.session.add(new_wishlist_item)
    db.session.commit()
    
    # Get updated wishlist count
    wishlist_count = WishlistItem.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'success': True,
        'message': 'Item added to wishlist!',
        'wishlist_count': wishlist_count
    })

@wishlist_bp.route('/api/wishlist/remove', methods=['POST'])
@login_required
@csrf.exempt
def remove_from_wishlist():
    # Get data from request
    data = request.get_json()
    wishlist_item_id = data.get('wishlist_item_id')
    
    if not wishlist_item_id:
        return jsonify({'success': False, 'message': 'Wishlist item ID is required'}), 400
    
    # Get wishlist item and delete
    wishlist_item = WishlistItem.query.filter_by(
        id=wishlist_item_id, 
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Item removed from wishlist!'
    })

@wishlist_bp.route('/api/wishlist/toggle', methods=['POST'])
@login_required
@csrf.exempt
def toggle_wishlist():
    # Get data from request
    data = request.get_json()
    product_id = data.get('product_id')
    
    if not product_id:
        return jsonify({'success': False, 'message': 'Product ID is required'}), 400
    
    # Check if product exists
    product = Product.query.get_or_404(product_id)
    
    # Check if item is already in wishlist
    wishlist_item = WishlistItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if wishlist_item:
        # Remove from wishlist if already exists
        db.session.delete(wishlist_item)
        db.session.commit()
        action = 'removed'
    else:
        # Add to wishlist if not exists
        new_wishlist_item = WishlistItem(
            user_id=current_user.id,
            product_id=product_id
        )
        db.session.add(new_wishlist_item)
        db.session.commit()
        action = 'added'
    
    # Get updated wishlist count
    wishlist_count = WishlistItem.query.filter_by(user_id=current_user.id).count()
    
    return jsonify({
        'success': True,
        'action': action,
        'message': f'Item {action} to wishlist!',
        'wishlist_count': wishlist_count
    })

@wishlist_bp.route('/api/wishlist/count')
@login_required
@csrf.exempt
def get_wishlist_count():
    """Get the number of items in the wishlist"""
    count = WishlistItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})
