from app import app, db
from models import Product
from datetime import datetime

# Example product data
products = [
    {
        "name": "Professional DSLR Camera",
        "price": 1299.99,
        "category": "Electronics",
        "description": "High-end professional DSLR camera with 24.2MP sensor, 4K video recording, and advanced autofocus system. Perfect for professional photographers and serious enthusiasts.\n\nFeatures:\n- 24.2MP APS-C CMOS Sensor\n- EXPEED 5 Image Processor\n- 3.2\" 2.36m-Dot Tilting Touchscreen LCD\n- 4K UHD Video Recording at 30 fps\n- Multi-CAM 20K 153-Point AF System\n- Native ISO 51200, Extended to ISO 1640000\n- 10 fps Shooting for Up to 200 Frames\n- Built-In Wi-Fi, Bluetooth and NFC\n- Weather-Sealed Design",
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 15
    },
    {
        "name": "Wireless Noise-Cancelling Headphones",
        "price": 249.99,
        "category": "Electronics",
        "description": "Premium wireless headphones with industry-leading noise cancellation, exceptional sound quality, and long battery life. Immerse yourself in your music without distractions.\n\nFeatures:\n- Industry-leading noise cancellation\n- 30-hour battery life\n- Quick charge (5 hours of playback with 10-minute charge)\n- Touch controls for easy operation\n- High-quality built-in microphone for calls\n- Comfortable over-ear design\n- Foldable design for easy storage",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 25
    },
    {
        "name": "Smart Fitness Watch",
        "price": 199.99,
        "category": "Electronics",
        "description": "Advanced fitness tracker with heart rate monitoring, GPS, sleep tracking, and water resistance. Stay connected and monitor your health metrics with precision.\n\nFeatures:\n- Advanced heart rate monitoring\n- Built-in GPS for accurate pace and distance\n- Water resistant to 50 meters\n- Sleep tracking with insights\n- 7+ day battery life\n- Smartphone notifications\n- Multiple exercise modes\n- Stress tracking and guided breathing sessions",
        "image_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd6b4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 30
    },
    {
        "name": "Premium Leather Wallet",
        "price": 79.99,
        "category": "Fashion",
        "description": "Handcrafted genuine leather wallet with RFID blocking technology, multiple card slots, and sleek design. Combines classic style with modern functionality.\n\nFeatures:\n- Genuine full-grain leather\n- RFID blocking technology\n- 8 card slots and 2 currency compartments\n- ID window\n- Slim profile design\n- Gift box included\n- Available in black, brown, and tan",
        "image_url": "https://images.unsplash.com/photo-1627123423530-39b6c611b322?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 50
    },
    {
        "name": "Ultra-Thin Laptop",
        "price": 1499.99,
        "category": "Electronics",
        "description": "Ultra-thin, lightweight laptop with powerful performance, stunning display, and all-day battery life. Perfect for professionals and students on the go.\n\nFeatures:\n- Latest Intel Core i7 processor\n- 16GB RAM\n- 512GB SSD storage\n- 14\" 4K Ultra HD display\n- Backlit keyboard\n- Fingerprint reader\n- 12+ hour battery life\n- Weighs just 2.6 pounds\n- Windows 11 Pro",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 10
    },
    {
        "name": "Artisan Coffee Maker",
        "price": 129.99,
        "category": "Home",
        "description": "Premium coffee maker with precision brewing technology, adjustable settings, and elegant design. For coffee enthusiasts who appreciate quality and craftsmanship.\n\nFeatures:\n- PID temperature control\n- Adjustable brew strength\n- Pre-infusion function\n- 10-cup glass carafe\n- Stainless steel construction\n- Programmable timer\n- Auto shut-off\n- Water filtration system included\n- BPA-free components",
        "image_url": "https://images.unsplash.com/photo-1526170160160-1a5eb242ab58?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 20
    },
    {
        "name": "Ergonomic Office Chair",
        "price": 349.99,
        "category": "Home",
        "description": "Fully adjustable ergonomic office chair with lumbar support, breathable mesh, and premium build quality. Designed for comfort during long working sessions.\n\nFeatures:\n- Adjustable lumbar support\n- Breathable mesh back\n- Adjustable armrests, seat height, and tilt\n- Heavy-duty aluminum base\n- Smooth-rolling casters\n- Weight capacity of 300 lbs\n- Headrest included\n- 5-year warranty",
        "image_url": "https://images.unsplash.com/photo-1561631541-b31e4e15e414?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 15
    },
    {
        "name": "Smart Home Security System",
        "price": 299.99,
        "category": "Electronics",
        "description": "Comprehensive smart home security system with HD cameras, motion sensors, and smartphone integration. Keep your home safe with real-time alerts and monitoring.\n\nFeatures:\n- 1080p HD cameras with night vision\n- Motion and door/window sensors\n- Mobile app control and notifications\n- Two-way audio communication\n- Local and cloud storage options\n- Works with Alexa and Google Assistant\n- Easy DIY installation\n- No monthly fees",
        "image_url": "https://images.unsplash.com/photo-1563624475-e337a646b373?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 12
    },
    {
        "name": "Modern Ceramic Vase Set",
        "price": 59.99,
        "category": "Home",
        "description": "Set of 3 handcrafted ceramic vases in complementary designs and sizes. Perfect for displaying flowers or as standalone decorative pieces.\n\nFeatures:\n- Handcrafted from high-quality ceramic\n- Set of 3 different sizes (small, medium, large)\n- Modern, minimalist design\n- Glazed finish in neutral tones\n- Water-tight for fresh flowers\n- Makes a perfect housewarming gift\n- Each piece is unique with slight variations",
        "image_url": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 25
    },
    {
        "name": "Designer Sunglasses",
        "price": 169.99,
        "category": "Fashion",
        "description": "Premium designer sunglasses with polarized lenses, UV protection, and lightweight frame. Combine style with eye protection in these versatile shades.\n\nFeatures:\n- Polarized lenses reduce glare\n- 100% UV protection\n- Lightweight acetate frame\n- Scratch-resistant coating\n- Includes protective case and cleaning cloth\n- Classic design that complements any face shape\n- Available in multiple colors",
        "image_url": "https://images.unsplash.com/photo-1577803645773-f96470509666?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 35
    },
    {
        "name": "Organic Cotton Bedding Set",
        "price": 129.99,
        "category": "Home",
        "description": "Luxurious 100% organic cotton bedding set including duvet cover, fitted sheet, and pillowcases. Experience the perfect blend of comfort and sustainability.\n\nFeatures:\n- 100% GOTS-certified organic cotton\n- 400 thread count for luxurious softness\n- Includes duvet cover, fitted sheet, and 2 pillowcases\n- Natural dyes with no harsh chemicals\n- Breathable fabric for year-round comfort\n- Easy care: machine washable\n- Available in queen and king sizes\n- Multiple colors available",
        "image_url": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 20
    },
    {
        "name": "Professional Chef's Knife",
        "price": 89.99,
        "category": "Home",
        "description": "High-carbon stainless steel chef's knife with ergonomic handle and precision-honed edge. The essential tool for any serious home cook or professional chef.\n\nFeatures:\n- 8-inch blade made from high-carbon stainless steel\n- Full tang construction for balance and durability\n- Ergonomic handle for comfortable grip\n- Hand-honed edge for exceptional sharpness\n- Precision forged with perfect weight distribution\n- Versatile for chopping, slicing, dicing, and mincing\n- Includes protective sheath\n- Lifetime warranty",
        "image_url": "https://images.unsplash.com/photo-1593618998160-e34014e67546?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 30
    }
]

def seed_database():
    with app.app_context():
        # Check if products already exist
        existing_count = Product.query.count()
        if existing_count > 0:
            print(f"{existing_count} products already exist in the database. Skipping seed.")
            return
        
        # Add products to database
        for product_data in products:
            product = Product(
                name=product_data["name"],
                price=product_data["price"],
                category=product_data["category"],
                description=product_data["description"],
                image_url=product_data["image_url"],
                stock=product_data["stock"],
                created_at=datetime.utcnow()
            )
            db.session.add(product)
        
        # Commit changes
        db.session.commit()
        print(f"Added {len(products)} products to the database.")

if __name__ == "__main__":
    seed_database()