# check_models.py
from app import create_app, db
from app.models import Location

app = create_app()

with app.app_context():
    # Check Location model columns
    print("Location model columns:")
    for column in Location.__table__.columns:
        print(f"   {column.name}: {column.type}")