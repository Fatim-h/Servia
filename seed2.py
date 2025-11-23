# seed2.py
from server import create_app, db
from backend.models import *
from werkzeug.security import generate_password_hash
from datetime import date, time

app = create_app()

with app.app_context():
    print("DB URL:", app.config["SQLALCHEMY_DATABASE_URI"])

    # --------------------------
    # New Users
    # --------------------------
    auth_charlie2 = AuthData(name="charlie2", role="user")
    auth_charlie2.password_hash = generate_password_hash("password123")
    user_charlie2 = User(name="Charlie 2", age=28, email="charlie2@example.com", auth=auth_charlie2)

    auth_diana2 = AuthData(name="diana2", role="user")
    auth_diana2.password_hash = generate_password_hash("password123")
    user_diana2 = User(name="Diana 2", age=35, email="diana2@example.com", auth=auth_diana2)

    db.session.add_all([user_charlie2, user_diana2])
    db.session.commit()

    # --------------------------
    # New Causes
    # --------------------------
    cause3 = Cause(
        name="Clean Oceans",
        description="Initiative to remove plastic from oceans",
        user=user_charlie2,
        verified=True
    )
    cause4 = Cause(
        name="Help Homeless",
        description="Providing shelter and food for homeless people",
        user=user_diana2,
        verified=True
    )

    db.session.add_all([cause3, cause4])
    db.session.commit()

    # --------------------------
    # New NGOs
    # --------------------------
    ngo3 = NGO(cause=cause3, year_est=2010, age=15)
    ngo4 = NGO(cause=cause4, year_est=2018, age=7)

    db.session.add_all([ngo3, ngo4])
    db.session.commit()

    # --------------------------
    # New Events
    # --------------------------
    event3 = Event(cause_id=cause3.cause_id, ngo_id=ngo3.ngo_id, capacity=80, date=date(2025, 11, 30), time=time(9, 0))
    event4 = Event(cause_id=cause4.cause_id, ngo_id=ngo4.ngo_id, capacity=60, date=date(2025, 12, 5), time=time(11, 0))

    db.session.add_all([event3, event4])
    db.session.commit()

    # --------------------------
    # Locations
    # --------------------------
    loc3 = Location(country="UK", city="London", latitude=51.5074, longitude=-0.1278,
                    contact_no="111-222-3333", address="789 Thames St", cause=cause3)
    loc4 = Location(country="Canada", city="Toronto", latitude=43.6532, longitude=-79.3832,
                    contact_no="444-555-6666", address="321 Maple Ave", cause=cause4)

    db.session.add_all([loc3, loc4])
    db.session.commit()

    # --------------------------
    # Account Details
    # --------------------------
    acc3 = AccountDetails(iban="GB1234567890", acc_name="Charlie 2 Account", user=user_charlie2, cause=cause3)
    acc4 = AccountDetails(iban="CA0987654321", acc_name="Diana 2 Account", user=user_diana2, cause=cause4)

    db.session.add_all([acc3, acc4])
    db.session.commit()

    # --------------------------
    # Donations
    # --------------------------
    donation3 = Donation(amount=75.0, user=user_diana2, cause=cause3)
    donation4 = Donation(amount=120.0, user=user_charlie2, cause=cause4)

    db.session.add_all([donation3, donation4])
    db.session.commit()

    # --------------------------
    # Volunteers
    # --------------------------
    vol3 = Volunteer(user=user_charlie2, cause=cause3)
    vol4 = Volunteer(user=user_diana2, cause=cause4)

    db.session.add_all([vol3, vol4])
    db.session.commit()

    # --------------------------
    # Feedback
    # --------------------------
    fb3 = Feedback(user=user_diana2, cause=cause3, comment="Very important work!", rating=5)
    fb4 = Feedback(user=user_charlie2, cause=cause4, comment="Happy to help!", rating=4)

    db.session.add_all([fb3, fb4])
    db.session.commit()

    # --------------------------
    # User Contacts & Socials
    # --------------------------
    uc3 = UserContact(contact="222-333-4444", user=user_charlie2)
    uc4 = UserContact(contact="555-666-7777", user=user_diana2)
    us3 = UserSocials(social="@charlie2_social", user=user_charlie2)
    us4 = UserSocials(social="@diana2_social", user=user_diana2)

    db.session.add_all([uc3, uc4, us3, us4])
    db.session.commit()

    # --------------------------
    # Cause Contacts & Socials
    # --------------------------
    cc3 = CauseContact(contact="777-888-9999", cause=cause3)
    cc4 = CauseContact(contact="000-111-2222", cause=cause4)
    cs3 = CauseSocials(social="@cleanoceans", cause=cause3)
    cs4 = CauseSocials(social="@helphomeless", cause=cause4)

    db.session.add_all([cc3, cc4, cs3, cs4])
    db.session.commit()

    print("✅ Additional seed data added successfully!")