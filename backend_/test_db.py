# test_db.py
from app import create_app, db
from app.models import Category, NGO

app = create_app()

with app.app_context():
    # Check if tables exist and have data
    categories = Category.query.all()
    ngos = NGO.query.all()
    
    print(f"Categories: {len(categories)}")
    print(f"NGOs: {len(ngos)}")
    
    for ngo in ngos:
        print(f"NGO: {ngo.name} - {ngo.location.city if ngo.location else 'No location'}")