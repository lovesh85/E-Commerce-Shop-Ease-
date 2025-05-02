from app import app, db
from models import User
from datetime import datetime

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@shopease.com').first()
        
        if not admin:
            # Create admin user
            admin = User(
                name='Admin User',
                email='admin@shopease.com',
                is_admin=True,
                created_at=datetime.utcnow()
            )
            # Set password
            admin.set_password('admin123')
            
            # Add to database
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
            print("Email: admin@shopease.com")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
            print("Email: admin@shopease.com")

if __name__ == "__main__":
    create_admin_user()