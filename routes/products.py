from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db, csrf
from models import Product, CartItem, WishlistItem

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    # Get featured products (for homepage)
    featured_products = Product.query.limit(8).all()
    
    # Get newest products
    newest_products = Product.query.order_by(Product.created_at.desc()).limit(6).all()
    
    # Get categories for navigation
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]
    
    # Get products by category (for category sections)
    category_products = {}
    for category in categories[:4]:  # Limit to first 4 categories
        category_products[category] = Product.query.filter_by(category=category).limit(4).all()
    
    return render_template('index.html', 
                          featured_products=featured_products,
                          newest_products=newest_products,
                          categories=categories,
                          category_products=category_products)

@products_bp.route('/products')
def product_list():
    # Get query parameters
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    
    # Base query
    query = Product.query
    
    # Filter by category if provided
    if category:
        query = query.filter_by(category=category)
    
    # Filter by search term if provided
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            )
        )
    
    # Get all categories for filter sidebar
    categories = db.session.query(Product.category).distinct().all()
    categories = [category[0] for category in categories]
    
    # Execute query and get products
    products = query.all()
    
    return render_template('products.html', 
                          products=products, 
                          categories=categories,
                          current_category=category,
                          search_term=search)

@products_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Check if product is in user's cart or wishlist (if logged in)
    in_cart = False
    in_wishlist = False
    
    if current_user.is_authenticated:
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        wishlist_item = WishlistItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        in_cart = cart_item is not None
        in_wishlist = wishlist_item is not None
    
    # Get related products in the same category
    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(4).all()
    
    return render_template('product_detail.html', 
                          product=product,
                          in_cart=in_cart,
                          in_wishlist=in_wishlist,
                          related_products=related_products)

@products_bp.route('/api/products')
@csrf.exempt
def api_products():
    """API endpoint for product data (used by JavaScript frontend)"""
    products = Product.query.all()
    
    # Convert products to JSON serializable format
    products_data = [{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category,
        'image_url': p.image_url,
        'stock': p.stock
    } for p in products]
    
    return jsonify(products_data)
