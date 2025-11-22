from app import create_app, db
from app.models import Category, User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Add categories
    categories = ['Education', 'Healthcare', 'Environment', 'Women Empowerment', 'Poverty Alleviation']
    for cat_name in categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
    
    # Add admin user
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin', 
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
    
    db.session.commit()
    print("Sample data added successfully!")