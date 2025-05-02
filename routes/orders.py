from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
import os
from app import db, csrf
from models import Order, OrderItem, CartItem, Product

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/checkout')
@login_required
def checkout():
    # Get all cart items for current user
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Redirect to cart if cart is empty
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # Convert to INR (as per our conversion in the template)
    inr_total = int(total * 75)
    
    # Add 10% tax
    final_amount = int(inr_total * 1.1)
    
    # Get user details for checkout form
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        total=total,
        amount=final_amount,
        currency='INR',
        email=current_user.email,
        name=current_user.name
    )

@orders_bp.route('/place-order', methods=['POST'])
@login_required
def place_order():
    # Get payment details from form
    card_number = request.form.get('card_number', '')
    card_holder = request.form.get('card_holder', '')
    expiry_date = request.form.get('expiry_date', '')
    cvv = request.form.get('cvv', '')
    
    # Get cart items
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # Calculate total
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # Validate form data (basic validation)
    if not card_number or not card_holder or not expiry_date or not cvv:
        flash('Please fill in all payment details.', 'danger')
        return redirect(url_for('orders.checkout'))
    
    # Set payment status (this would normally be returned by a payment provider)
    payment_status = 'Paid'
    
    # Create new order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        payment_status=payment_status,
        order_status='Pending'
    )
    db.session.add(new_order)
    db.session.flush()  # Get the order ID
    
    # Create order items
    for cart_item in cart_items:
        # Check if product has enough stock
        if cart_item.product.stock < cart_item.quantity:
            flash(f'Not enough stock for {cart_item.product.name}!', 'danger')
            db.session.rollback()
            return redirect(url_for('cart.view_cart'))
        
        # Create order item
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        db.session.add(order_item)
        
        # Update product stock
        cart_item.product.stock -= cart_item.quantity
    
    # Clear cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
    
    db.session.commit()
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('orders.order_success', order_id=new_order.id))

@orders_bp.route('/order-success/<int:order_id>')
@login_required
def order_success(order_id):
    # Get order
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    return render_template('order_success.html', order=order)

@orders_bp.route('/orders')
@login_required
def order_history():
    # Get all orders for current user
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    return render_template('order_history.html', orders=orders)

@orders_bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    # Get order
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    
    return render_template('order_detail.html', order=order)
