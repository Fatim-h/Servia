from app import create_app, db
from werkzeug.security import generate_password_hash

app = create_app()

def reset_database():
    with app.app_context():
        print("Resetting database...")
        
        # Drop all tables
        db.drop_all()
        print("Dropped all tables")
        
        # Create all tables with new schema
        db.create_all()
        print("Created all tables with new schema")
        
        print("Database reset complete!")

if __name__ == '__main__':
    reset_database()