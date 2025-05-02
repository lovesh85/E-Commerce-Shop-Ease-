# ShopEase - Modern eCommerce Platform

ShopEase is a comprehensive eCommerce website built with Flask and PostgreSQL, offering a seamless online shopping experience with a modern, responsive design. The platform provides both customer-facing features and robust admin capabilities, making it a complete solution for online retail.

![ShopEase Screenshot](https://images.unsplash.com/photo-1607082349566-187342175e2f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80)

## Table of Contents
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Admin Dashboard](#admin-dashboard)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Security Measures](#security-measures)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Features

### Customer Features
- **User Authentication**:
  - Secure login and registration system
  - Password hashing and validation
  - Remember me functionality
  - Profile management
- **Product Browsing**:
  - Browse all products or by category
  - Sort products by price, popularity, or newest
  - Search products by name or description
  - Filter products by price range or availability
- **Product Details**:
  - High-quality product images
  - Detailed descriptions and specifications
  - Price in Indian Rupees (₹)
  - Current stock status
- **Shopping Cart**:
  - Add products to cart
  - Update quantities directly from cart
  - Remove items individually
  - Cart persistence between sessions
  - Real-time cart total calculation
- **Wishlist**:
  - Add/remove products to wishlist
  - Move items from wishlist to cart
  - Persistent wishlist between sessions
- **Checkout Process**:
  - Simple and secure checkout form
  - Card information collection
  - Order summary before confirmation
  - Order confirmation with details
- **Order History**:
  - View all past orders
  - Track order status (Pending, Shipped, Delivered, Cancelled)
  - Order details including items and total

### Admin Features
- **Dashboard**:
  - Overview with key metrics (total sales, orders, users)
  - Sales charts by time period (daily, weekly, monthly)
  - Recent orders with status
  - Product inventory alerts for low stock
  - Bar graph showing sales by category
- **Product Management**:
  - Add new products with validation
  - Edit existing product information
  - Update stock levels
  - Delete products
  - Bulk operations on products
- **Order Management**:
  - View all orders with filtering options
  - Update order status (Pending, Shipped, Delivered, Cancelled)
  - View detailed order information
  - Search orders by customer or order ID
- **User Management**:
  - View all user accounts
  - Toggle admin privileges
  - Search users by email or name
- **Sales Analytics**:
  - Visual charts showing sales trends
  - Product performance analysis
  - Category performance comparison
  - Revenue tracking over time

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database interactions
- **Flask-Login**: User authentication and session management
- **Flask-WTF**: Form handling and validation
- **Werkzeug**: Password hashing and security utilities
- **Jinja2**: Template engine for dynamic HTML

### Database
- **PostgreSQL**: Robust relational database
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **Database Migrations**: Schema management and updates

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Client-side functionality
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization for admin dashboard
- **AJAX**: Asynchronous operations for cart and wishlist

### Deployment
- **Gunicorn**: WSGI HTTP Server
- **Replit**: Hosting platform

## Database Schema

The application uses a relational database with the following primary tables:

### Users Table
- `id`: Primary key
- `name`: User's full name
- `email`: User's email (unique)
- `password_hash`: Securely hashed password
- `is_admin`: Boolean for admin status
- `created_at`: Registration timestamp

### Products Table
- `id`: Primary key
- `name`: Product name
- `price`: Product price (in USD, converted to INR for display)
- `category`: Product category
- `description`: Detailed product description
- `image_url`: URL to product image
- `stock`: Current stock quantity
- `created_at`: Product addition timestamp

### Orders Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `total_amount`: Order total amount
- `payment_status`: Status of payment (Paid, Failed, Pending)
- `order_status`: Status of order (Pending, Shipped, Delivered, Cancelled)
- `created_at`: Order placement timestamp

### Order Items Table
- `id`: Primary key
- `order_id`: Foreign key to Orders
- `product_id`: Foreign key to Products
- `quantity`: Quantity ordered
- `price`: Price at time of purchase

### Cart Items Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `product_id`: Foreign key to Products
- `quantity`: Quantity in cart
- Unique constraint on user_id and product_id

### Wishlist Items Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `product_id`: Foreign key to Products
- `added_at`: Timestamp when added to wishlist
- Unique constraint on user_id and product_id

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- Git (for cloning the repository)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd shopease
   ```

2. **Set up PostgreSQL database**
   - Create a new PostgreSQL database
   - Note your database connection credentials

3. **Set environment variables**
   Create a `.env` file in the project root with:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/shopease
   SECRET_KEY=your_secure_secret_key
   ```

4. **Install dependencies**
   ```bash
   pip install -r project_requirements.txt
   ```

5. **Initialize the database**
   ```bash
   # Seed the database with sample products
   python seed_products.py
   
   # Create admin user
   python create_admin.py
   ```

6. **Run the application**
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```
   
   For development:
   ```bash
   python main.py
   ```

7. **Access the application**
   Open your browser and go to `http://localhost:5000`

## Usage Guide

### Customer Journey

1. **Registration and Login**
   - Register a new account via the Register page
   - Login with your email and password
   - Optional: Use "Remember Me" for persistent login

2. **Browsing Products**
   - View featured products on the homepage
   - Browse all products or by category
   - Use search functionality to find specific products
   - Sort and filter products as needed

3. **Product Interaction**
   - Click on a product to view details
   - Add products to cart or wishlist
   - Adjust quantities directly from the cart page
   - Move items between wishlist and cart

4. **Checkout Process**
   - Review cart and confirm items
   - Enter shipping information
   - Enter payment details
   - Confirm order and receive order number

5. **Order Management**
   - View order history in user profile
   - Track status of current orders
   - View details of past orders

### Admin Journey

1. **Accessing Admin Dashboard**
   - Login with admin credentials (admin@shopease.com / admin123)
   - Access dashboard via user dropdown menu

2. **Managing Products**
   - View all products in the Products section
   - Add new products through the Add Product form
   - Edit existing products as needed
   - Remove products that are no longer available

3. **Managing Orders**
   - Review incoming orders from the Orders section
   - Update order status as orders are processed
   - View detailed information for specific orders

4. **User Management**
   - View and search user accounts
   - Toggle admin status for users
   - Monitor user activity

5. **Analytics and Reporting**
   - View sales charts and metrics
   - Track product performance
   - Monitor revenue trends

## Admin Dashboard

The admin dashboard provides comprehensive tools for store management:

### Dashboard Overview
- **Key Metrics Cards**: Total sales, orders, products, and users
- **Sales Charts**: Visual representation of sales data
- **Recent Orders**: Quick view of latest orders with status
- **Low Stock Alerts**: Products that need restocking

### Product Management
The product management interface includes:
- **Product Listing**: Sortable and searchable table of all products
- **Add Product Form**: Form to add new products with validation
- **Edit Product**: Update product details and stock levels
- **Delete Product**: Remove products from the catalog

### Order Management
The order management interface includes:
- **Order Listing**: All orders with filtering and sorting
- **Order Details**: Complete information about each order
- **Status Update**: Change order status (Pending, Shipped, etc.)
- **Customer Information**: Access to purchaser details

## API Endpoints

ShopEase provides several API endpoints for client-side interactions:

### Product APIs
- `GET /api/products`: Returns a list of all products
  - Optional query parameters: category, sort, search

### Cart APIs
- `GET /api/cart/count`: Returns the current number of items in cart
- `POST /api/cart/add`: Adds a product to the cart
  - Required body: product_id, quantity
- `POST /api/cart/update`: Updates cart item quantity
  - Required body: cart_item_id, quantity
- `POST /api/cart/remove`: Removes an item from the cart
  - Required body: cart_item_id

### Wishlist APIs
- `GET /api/wishlist/count`: Returns the current number of items in wishlist
- `POST /api/wishlist/add`: Adds a product to the wishlist
  - Required body: product_id
- `POST /api/wishlist/remove`: Removes an item from the wishlist
  - Required body: wishlist_item_id
- `POST /api/wishlist/toggle`: Toggles a product in the wishlist
  - Required body: product_id

## Project Structure

```
shopease/
├── routes/                       # Route definitions
│   ├── admin.py                  # Admin dashboard routes
│   ├── auth.py                   # Authentication routes
│   ├── cart.py                   # Shopping cart routes
│   ├── orders.py                 # Order processing routes
│   ├── products.py               # Product listing routes
│   └── wishlist.py               # Wishlist management routes
│
├── static/                       # Static assets
│   ├── css/                      # CSS stylesheets
│   │   └── style.css             # Main stylesheet
│   ├── js/                       # JavaScript files
│   │   ├── admin.js              # Admin dashboard functionality
│   │   ├── cart.js               # Cart functionality
│   │   ├── main.js               # Core functionality
│   │   └── wishlist.js           # Wishlist functionality
│
├── templates/                    # Jinja2 templates
│   ├── admin/                    # Admin templates
│   │   ├── dashboard.html        # Admin dashboard
│   │   ├── products.html         # Product management
│   │   └── orders.html           # Order management
│   ├── auth/                     # Authentication templates
│   │   ├── login.html            # Login page
│   │   └── register.html         # Registration page
│   ├── cart/                     # Cart templates
│   │   └── cart.html             # Shopping cart
│   ├── orders/                   # Order templates
│   │   ├── checkout.html         # Checkout page
│   │   └── order_history.html    # Order history
│   ├── products/                 # Product templates
│   │   ├── index.html            # Homepage
│   │   ├── product_list.html     # Product listing
│   │   └── product_detail.html   # Product details
│   ├── base.html                 # Base template with layout
│
├── app.py                        # Application factory
├── forms.py                      # WTForms definitions
├── main.py                       # Application entry point
├── models.py                     # Database models
├── utils.py                      # Utility functions
├── seed_products.py              # Database seeding script
├── create_admin.py               # Admin user creation script
└── project_requirements.txt      # Project dependencies
```

## Security Measures

ShopEase implements several security best practices:

- **Password Security**:
  - Passwords are hashed using Werkzeug's security functions
  - Minimum password length enforcement
  - Password strength validation

- **Form Protection**:
  - CSRF protection on all forms
  - Input validation and sanitization
  - Form field validation with WTForms

- **Session Security**:
  - Secure session management with Flask-Login
  - Session timeout for inactive users
  - HTTPS enforcement in production

- **Database Security**:
  - Parameterized queries through SQLAlchemy
  - Protection against SQL injection
  - Relationship integrity with foreign keys

- **API Security**:
  - CSRF protection for all AJAX requests
  - Authentication checks for protected endpoints
  - Rate limiting for API requests

## Contributing

We welcome contributions to improve ShopEase! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Use descriptive variable and function names
- Add comments for complex logic
- Write tests for new features
- Update documentation for any changes

## Troubleshooting

### Common Issues and Solutions

**Database Connection Errors**
- Check if your PostgreSQL service is running
- Verify DATABASE_URL environment variable is correctly formatted
- Ensure your database user has proper permissions

**Missing Dependencies**
- Run `pip install -r project_requirements.txt` to install all dependencies
- Check for any error messages during installation

**JavaScript Console Errors**
- Check browser console for specific error messages
- Verify CSRF token is properly included in AJAX requests

**Template Rendering Issues**
- Check for typos in template variable names
- Ensure all required variables are passed to templates

**Server Start-up Issues**
- Check for port conflicts (default is 5000)
- Verify environment variables are properly set
- Check for syntax errors in Python files