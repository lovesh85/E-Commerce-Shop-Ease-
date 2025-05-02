from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from models import Product, User, Order
from forms import ProductForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin middleware to check if user is admin
@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Access denied. You must be an admin to access this page.', 'danger')
        return redirect(url_for('products.index'))

@admin_bp.route('/')
@login_required
def dashboard():
    # Get summary data for dashboard
    total_products = Product.query.count()
    total_users = User.query.filter_by(is_admin=False).count()
    total_orders = Order.query.count()
    
    # Get latest orders
    latest_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Get out of stock products
    out_of_stock = Product.query.filter(Product.stock == 0).count()
    
    # Total revenue
    revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # Get category data for bar chart
    categories = db.session.query(Product.category, 
                                 db.func.count(Product.id).label('count'))\
                          .group_by(Product.category).all()
    
    # Prepare data for the chart
    category_names = [cat[0] for cat in categories]
    category_counts = [cat[1] for cat in categories]
    
    return render_template('admin/dashboard.html',
                          total_products=total_products,
                          total_users=total_users,
                          total_orders=total_orders,
                          latest_orders=latest_orders,
                          out_of_stock=out_of_stock,
                          revenue=revenue,
                          category_names=category_names,
                          category_counts=category_counts)

@admin_bp.route('/products')
@login_required
def products():
    # Get all products
    all_products = Product.query.all()
    
    return render_template('admin/products.html', products=all_products)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        # Create new product
        new_product = Product(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            description=form.description.data,
            image_url=form.image_url.data,
            stock=form.stock.data
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_edit.html', form=form, is_edit=False)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # Get product
    product = Product.query.get_or_404(product_id)
    
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        # Update product
        product.name = form.name.data
        product.price = form.price.data
        product.category = form.category.data
        product.description = form.description.data
        product.image_url = form.image_url.data
        product.stock = form.stock.data
        
        db.session.commit()
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
    
    return render_template('admin/product_edit.html', form=form, product=product, is_edit=True)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    # Get product
    product = Product.query.get_or_404(product_id)
    
    db.session.delete(product)
    db.session.commit()
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('admin.products'))

@admin_bp.route('/orders')
@login_required
def orders():
    # Get all orders
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    
    return render_template('admin/orders.html', orders=all_orders)

@admin_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    # Get order
    order = Order.query.get_or_404(order_id)
    
    return render_template('admin/order_detail.html', order=order)

@admin_bp.route('/orders/update-status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    # Get order
    order = Order.query.get_or_404(order_id)
    
    # Get new status
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'Shipped', 'Delivered', 'Cancelled']:
        order.order_status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}!', 'success')
    else:
        flash('Invalid status!', 'danger')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin_bp.route('/users')
@login_required
def users():
    # Get all non-admin users
    all_users = User.query.filter_by(is_admin=False).all()
    
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/users/toggle-status/<int:user_id>', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    # Get user
    user = User.query.get_or_404(user_id)
    
    # Cannot deactivate self
    if user.id == current_user.id:
        flash('You cannot deactivate yourself!', 'danger')
        return redirect(url_for('admin.users'))
    
    # Toggle active status (not yet implemented in model, would need an is_active field)
    # For now, we'll just show a message
    flash(f'User status toggled (would deactivate {user.name})!', 'success')
    
    return redirect(url_for('admin.users'))
