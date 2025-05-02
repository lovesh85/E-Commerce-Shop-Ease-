from app import app, db
from models import Product
from datetime import datetime

# Additional products to add to the database
more_products = [
    {
        "name": "Premium Bluetooth Earbuds",
        "price": 159.99,
        "category": "Electronics",
        "description": "High-quality wireless earbuds with active noise cancellation, touch controls, and 30-hour battery life. Perfect for workouts and daily commuting.\n\nFeatures:\n- Active noise cancellation technology\n- Bluetooth 5.2 connectivity\n- IPX7 waterproof rating\n- Touch controls for calls and music\n- 8 hours playtime, 30 hours with charging case\n- Comes with 3 sizes of ear tips\n- Quick charging: 10 minutes for 2 hours playback",
        "image_url": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 45
    },
    {
        "name": "Smart Home Assistant",
        "price": 129.99,
        "category": "Electronics",
        "description": "Voice-controlled smart home assistant with premium sound quality and integrated smart home controls. Control your home with just your voice.\n\nFeatures:\n- 360° omni-directional sound\n- Voice recognition from across the room\n- Compatible with major smart home platforms\n- Controls lights, thermostats, locks and more\n- Streams music from popular services\n- Answers questions and provides information\n- Multi-room synchronization",
        "image_url": "https://images.unsplash.com/photo-1518444065439-e933c06ce9cd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 28
    },
    {
        "name": "Stainless Steel Cookware Set",
        "price": 249.99,
        "category": "Home",
        "description": "Professional-grade 10-piece stainless steel cookware set with tri-ply construction for even heat distribution. Perfect for serious home cooks.\n\nIncludes:\n- 8-inch and 10-inch frying pans\n- 2-quart and 3-quart saucepans with lids\n- 3.5-quart sauté pan with lid\n- 8-quart stockpot with lid\n\nFeatures:\n- Triple-layer construction with aluminum core\n- Oven safe up to 500°F\n- Dishwasher safe\n- Compatible with all cooktops including induction\n- Stay-cool handles for safe handling",
        "image_url": "https://images.unsplash.com/photo-1584990347533-814e75be9130?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 15
    },
    {
        "name": "Compact Air Purifier",
        "price": 199.99,
        "category": "Home",
        "description": "Advanced air purifier with True HEPA filter, captures 99.97% of airborne particles as small as 0.3 microns. Perfect for bedrooms, offices and small living spaces.\n\nFeatures:\n- 3-stage filtration: pre-filter, HEPA filter, activated carbon filter\n- Removes dust, pollen, pet dander, smoke and odors\n- Covers rooms up to 300 sq ft\n- Ultra-quiet operation as low as 24dB\n- Air quality sensor with auto mode\n- Filter replacement indicator\n- Timer function",
        "image_url": "https://images.unsplash.com/photo-1626436819821-df26d9eb0f7a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 22
    },
    {
        "name": "Designer Crossbody Bag",
        "price": 189.99,
        "category": "Fashion",
        "description": "Elegant crossbody bag crafted from premium leather with gold-tone hardware and adjustable strap. Combines style with functionality for any occasion.\n\nFeatures:\n- Genuine full-grain leather\n- Gold-tone hardware\n- Adjustable crossbody strap\n- Zippered main compartment\n- Interior pocket and card slots\n- Dimensions: 9\"L x 3\"W x 6\"H\n- Available in black, brown, and burgundy\n- Dust bag included",
        "image_url": "https://images.unsplash.com/photo-1591561954557-26941169b49e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 30
    },
    {
        "name": "Men's Minimalist Watch",
        "price": 219.99,
        "category": "Fashion",
        "description": "Sophisticated minimalist watch with Swiss movement, sapphire crystal, and Italian leather strap. Perfect for both casual and formal occasions.\n\nFeatures:\n- Swiss quartz movement\n- Sapphire crystal glass\n- 316L stainless steel case\n- Genuine Italian leather strap\n- 50m water resistance\n- 40mm case diameter\n- Date function\n- 2-year warranty",
        "image_url": "https://images.unsplash.com/photo-1539874754764-5a96559165b0?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 25
    },
    {
        "name": "Aromatherapy Essential Oil Diffuser",
        "price": 49.99,
        "category": "Home",
        "description": "Modern ultrasonic essential oil diffuser with 7-color LED lights and multiple mist settings. Create a calming atmosphere in any room.\n\nFeatures:\n- 300ml water capacity\n- 10+ hours of continuous operation\n- 7 changing LED light colors\n- Timer settings: 1h, 3h, 6h or continuous\n- Auto shut-off when water runs out\n- Whisper-quiet operation\n- BPA-free materials\n- Covers up to 300 sq ft",
        "image_url": "https://images.unsplash.com/photo-1608571423902-a13ae90f244f?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 40
    },
    {
        "name": "Indoor Plant Collection",
        "price": 79.99,
        "category": "Home",
        "description": "Set of 4 low-maintenance indoor plants in decorative ceramic pots. Perfect for purifying air and adding natural beauty to your home.\n\nIncludes:\n- Snake Plant (Sansevieria)\n- ZZ Plant (Zamioculcas)\n- Pothos (Epipremnum aureum)\n- Peace Lily (Spathiphyllum)\n\nFeatures:\n- Low-maintenance, ideal for beginners\n- Air-purifying qualities\n- 4 decorative ceramic pots included\n- Plants are approximately 6-10 inches tall\n- Care guide included",
        "image_url": "https://images.unsplash.com/photo-1604762512641-d6d5ebb40866?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 18
    },
    {
        "name": "Premium Yoga Mat",
        "price": 69.99,
        "category": "Sports",
        "description": "Eco-friendly, non-slip yoga mat with perfect cushioning and alignment markings. Ideal for all types of yoga, pilates, and floor exercises.\n\nFeatures:\n- 6mm thickness for joint protection\n- Non-slip textured surface\n- Alignment markings for proper form\n- Made from eco-friendly TPE material\n- Free from PVC, latex, and harmful chemicals\n- Closed-cell construction prevents sweat absorption\n- Includes carrying strap\n- Dimensions: 72\" x 26\"",
        "image_url": "https://images.unsplash.com/photo-1593164842264-854604db2260?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 35
    },
    {
        "name": "Wireless Charging Pad",
        "price": 29.99,
        "category": "Electronics",
        "description": "Fast wireless charging pad compatible with all Qi-enabled devices. Sleek, minimalist design with LED indicator and non-slip surface.\n\nFeatures:\n- 15W fast charging capability\n- Compatible with all Qi-enabled smartphones\n- LED charging indicator\n- Non-slip surface keeps phone secure\n- Ultra-slim design\n- Overcharge protection\n- Foreign object detection\n- USB-C cable included",
        "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 50
    },
    {
        "name": "Bamboo Bath Towel Set",
        "price": 89.99,
        "category": "Home",
        "description": "Luxury 6-piece bamboo bath towel set with exceptional softness and absorbency. Eco-friendly and hypoallergenic for sensitive skin.\n\nIncludes:\n- 2 bath towels (27\" x 54\")\n- 2 hand towels (16\" x 30\")\n- 2 washcloths (13\" x 13\")\n\nFeatures:\n- 70% bamboo, 30% organic cotton blend\n- 600 GSM for superior absorbency\n- Naturally antibacterial properties\n- Hypoallergenic and eco-friendly\n- Soft and gentle on sensitive skin\n- Quick-drying design\n- Available in multiple colors",
        "image_url": "https://images.unsplash.com/photo-1620626011761-996317b8d101?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 25
    },
    {
        "name": "Portable Bluetooth Speaker",
        "price": 79.99,
        "category": "Electronics",
        "description": "Waterproof portable Bluetooth speaker with 24-hour battery life and immersive 360° sound. Perfect for outdoor adventures and pool parties.\n\nFeatures:\n- IPX7 waterproof rating\n- 24-hour battery life\n- 360° immersive sound\n- Built-in microphone for calls\n- Bluetooth 5.0 connectivity\n- Durable fabric and rubber construction\n- Integrated carabiner for easy carrying\n- Pair two speakers for stereo sound",
        "image_url": "https://images.unsplash.com/photo-1589003077984-894e133f8525?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
        "stock": 30
    }
]

def add_more_products():
    with app.app_context():
        # Get existing product count
        existing_count = Product.query.count()
        
        # Add products
        for product_data in more_products:
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
        print(f"Added {len(more_products)} more products to the database. Total product count: {existing_count + len(more_products)}")

if __name__ == "__main__":
    add_more_products()