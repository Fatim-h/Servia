# cli.py
import os
from datetime import datetime
from backend import db
from backend.models import (
    AuthData, User, Cause, NGO, Event,
    AccountDetails, Donation, Feedback, Volunteer,
    UserContact, UserSocials, CauseContact, CauseSocials,
    Location
)
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import func

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")

# -----------------------------
# Create Flask app
# -----------------------------
app = Flask(__name__)
app.secret_key = "cli_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app, supports_credentials=True)

# -----------------------------
# CLI Functions
# -----------------------------
def create_sample_data():
    with app.app_context():
        print("=== Creating Sample Data ===")
        try:
            # Transaction example
            with db.session.begin():
                # Create users
                user1 = User(name="Alice", email="alice@example.com", age=28)
                user2 = User(name="Bob", email="bob@example.com", age=35)
                db.session.add_all([user1, user2])
                db.session.flush()  # flush to get IDs

                # Create causes
                cause1 = Cause(name="Save the Earth", description="Environmental NGO", user_id=user1.user_id)
                cause2 = Cause(name="Feed the Hungry", description="Food Charity", user_id=user2.user_id)
                db.session.add_all([cause1, cause2])
                db.session.flush()

                # Create donations
                donation1 = Donation(user_id=user1.user_id, cause_id=cause2.cause_id, amount=50)
                donation2 = Donation(user_id=user2.user_id, cause_id=cause1.cause_id, amount=100)
                db.session.add_all([donation1, donation2])

                # Create feedback
                feedback1 = Feedback(user_id=user1.user_id, cause_id=cause2.cause_id, comment="Great work!", rating=5)
                feedback2 = Feedback(user_id=user2.user_id, cause_id=cause1.cause_id, comment="Keep it up!", rating=4)
                db.session.add_all([feedback1, feedback2])

                # Create volunteers
                volunteer1 = Volunteer(user_id=user1.user_id, cause_id=cause1.cause_id)
                volunteer2 = Volunteer(user_id=user2.user_id, cause_id=cause2.cause_id)
                db.session.add_all([volunteer1, volunteer2])

            db.session.commit()
            print("Sample data created successfully!")

        except Exception as e:
            print("Error creating sample data:", e)
            db.session.rollback()

def advanced_queries():
    with app.app_context():
        print("\n=== Advanced SQLAlchemy Queries ===")

        # Total donations per cause
        print("\n-- Total Donations per Cause --")
        totals = db.session.query(
            Cause.name,
            func.sum(Donation.amount).label("total_donated")
        ).join(Donation, Donation.cause_id == Cause.cause_id).group_by(Cause.cause_id).all()
        for name, total in totals:
            print(f"{name}: ${total}")

        # Average rating per cause
        print("\n-- Average Feedback Rating per Cause --")
        avg_ratings = db.session.query(
            Cause.name,
            func.avg(Feedback.rating).label("avg_rating")
        ).join(Feedback, Feedback.cause_id == Cause.cause_id).group_by(Cause.cause_id).all()
        for name, avg in avg_ratings:
            print(f"{name}: {avg:.2f} stars")

        # List users with their number of donations
        print("\n-- Users and Number of Donations --")
        user_donations = db.session.query(
            User.name,
            func.count(Donation.donation_id).label("donation_count")
        ).join(Donation, Donation.user_id == User.user_id).group_by(User.user_id).all()
        for name, count in user_donations:
            print(f"{name}: {count} donations")

        # Join example: Users who donated to 'Feed the Hungry'
        print("\n-- Users who donated to 'Feed the Hungry' --")
        donors = db.session.query(User.name).join(Donation).join(Cause).filter(Cause.name == "Feed the Hungry").all()
        for (name,) in donors:
            print(name)

        # Transaction example: Add a new donation safely
        print("\n-- Adding a new donation inside a transaction --")
        try:
            with db.session.begin():
                user = User.query.first()
                cause = Cause.query.first()
                new_donation = Donation(user_id=user.user_id, cause_id=cause.cause_id, amount=75)
                db.session.add(new_donation)
            print("Donation added successfully!")
        except Exception as e:
            print("Failed to add donation:", e)
            db.session.rollback()

# -----------------------------
# Main CLI execution
# -----------------------------
if __name__ == "__main__":
    create_sample_data()
    advanced_queries()
