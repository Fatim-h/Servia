# populate.py
from server import create_app
from backend import db
from backend.models import (
    User, Cause, NGO, Event, Location, AccountDetails,
    Donation, Feedback, Volunteer, UserContact, UserSocials,
    CauseContact, CauseSocials, AuthData
)
from datetime import datetime

def populate_database():
    app = create_app()

    with app.app_context():
        # ---------------- DROP & CREATE ----------------
        db.drop_all()
        db.create_all()
        print("Database reset complete.")

        # ---------------- CREATE ADMIN ----------------
        admin = AuthData(
            id=0,
            name="admin",
            role="admin",
            verified=True
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin account created.")

        # ---------------- SAMPLE USERS ----------------
        user1 = User(name="Alice", email="alice@example.com", age=30, verified=True)
        user2 = User(name="Bob", email="bob@example.com", age=25, verified=True)

        db.session.add_all([user1, user2])
        db.session.commit()
        print("Sample users created.")

        # ---------------- SAMPLE CAUSES ----------------
        # NGO
        cause1 = Cause(
            name="Clean the Beach",
            description="Beach cleaning and ocean conservation project",
            logo=None,
            user_id=user1.user_id,
            verified=True
        )
        db.session.add(cause1)
        db.session.commit()

        ngo1 = NGO(cause_id=cause1.cause_id, year_est=2010, age=15)
        db.session.add(ngo1)

        # Event
        cause2 = Cause(
            name="Beach Cleanup Event",
            description="Volunteer event for cleaning the beach",
            logo=None,
            user_id=user2.user_id,
            verified=True
        )
        db.session.add(cause2)
        db.session.commit()

        event1 = Event(
            cause_id=cause2.cause_id,
            capacity=50,
            date=datetime.strptime("2025-12-01", "%Y-%m-%d").date(),
            time=datetime.strptime("10:00", "%H:%M").time(),
            ngo_id=cause1.cause_id
        )
        db.session.add(event1)
        db.session.commit()
        print("Sample causes (NGO + Event) created.")

        # ---------------- LOCATIONS ----------------
        loc1 = Location(
            country="India",
            city="Mumbai",
            latitude=19.0760,
            longitude=72.8777,
            address="Marine Drive",
            contact_no="1234567890",
            cause_id=cause1.cause_id
        )
        loc2 = Location(
            country="India",
            city="Mumbai",
            latitude=19.0900,
            longitude=72.8800,
            address="Juhu Beach",
            contact_no="0987654321",
            cause_id=cause2.cause_id
        )
        db.session.add_all([loc1, loc2])

        # ---------------- CONTACTS & SOCIALS ----------------
        user_contact = UserContact(contact="111-222-3333", user_id=user1.user_id)
        user_social = UserSocials(social="@alice", user_id=user1.user_id)
        cause_contact = CauseContact(contact="444-555-6666", cause_id=cause1.cause_id)
        cause_social = CauseSocials(social="@cleanbeach", cause_id=cause1.cause_id)
        db.session.add_all([user_contact, user_social, cause_contact, cause_social])

        # ---------------- ACCOUNT DETAILS ----------------
        acc_user = AccountDetails(
            iban="USERIBAN123",
            acc_name="Alice Account",
            user_id=user1.user_id
        )
        acc_cause = AccountDetails(
            iban="CAUSEIBAN123",
            acc_name="Clean Beach Account",
            cause_id=cause1.cause_id
        )
        db.session.add_all([acc_user, acc_cause])

        # ---------------- DONATIONS / FEEDBACK / VOLUNTEERS ----------------
        donation = Donation(amount=100.0, user_id=user1.user_id, cause_id=cause1.cause_id)
        feedback = Feedback(comment="Great initiative!", rating=5, user_id=user1.user_id, cause_id=cause1.cause_id)
        volunteer = Volunteer(user_id=user2.user_id, cause_id=cause2.cause_id)
        db.session.add_all([donation, feedback, volunteer])

        db.session.commit()
        print("All sample data populated successfully.")

if __name__ == "__main__":
    populate_database()

