# seed.py
from server import create_app, db
from backend.models import User, AuthData, Cause, Donation
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # --------------------------
    # Clear existing data (optional)
    # --------------------------
    Donation.query.delete()
    Cause.query.delete()
    User.query.delete()
    AuthData.query.delete()
    db.session.commit()

    # --------------------------
    # Create Users
    # --------------------------
    auth1 = AuthData(name="alice", role="user")
    auth1.password_hash = generate_password_hash("password123")
    user1 = User(name="Alice", age=30, email="alice@example.com", auth=auth1)

    auth2 = AuthData(name="bob", role="user")
    auth2.password_hash = generate_password_hash("password123")
    user2 = User(name="Bob", age=25, email="bob@example.com", auth=auth2)

    db.session.add_all([user1, user2])
    db.session.commit()

    # --------------------------
    # Create Causes
    # --------------------------
    cause1 = Cause(name="Feed the Kids", description="A charity to feed children in need", user=user1)
    cause2 = Cause(name="Plant Trees", description="Reforestation initiative", user=user2)

    db.session.add_all([cause1, cause2])
    db.session.commit()

    # --------------------------
    # Create Donations
    # --------------------------
    donation1 = Donation(amount=50.0, user=user2, cause=cause1)
    donation2 = Donation(amount=100.0, user=user1, cause=cause2)

    db.session.add_all([donation1, donation2])
    db.session.commit()

    print("✅ Seeded users, causes, and donations successfully!")