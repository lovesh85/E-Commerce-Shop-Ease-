import os
import logging
from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def admin_required(f):
    """
    Decorator to ensure user is an admin
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. You must be an admin to access this page.', 'danger')
            return redirect(url_for('products.index'))
        return f(*args, **kwargs)
    return decorated_function

def format_currency(amount):
    """
    Format amount as currency in Indian Rupees
    1 USD is approximately 75 INR (conversion rate used)
    """
    # Convert to rupees (approximate conversion rate)
    amount_in_rupees = amount * 75
    
    # Format with rupee symbol
    return f"₹{amount_in_rupees:.2f}"

def get_order_status_class(status):
    """
    Return Bootstrap class for order status
    """
    status_classes = {
        'Pending': 'bg-warning',
        'Shipped': 'bg-info',
        'Delivered': 'bg-success',
        'Cancelled': 'bg-danger'
    }
    return status_classes.get(status, 'bg-secondary')
