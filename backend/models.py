from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============================
#          AUTH
# ============================
class AuthData(db.Model):
    __tablename__ = 'auth_data'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user, ngo, event
    password_hash = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False)

    fk_id = db.Column(db.Integer, nullable=True)  # optional link to user or cause

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ============================
#           USER
# ============================
class User(db.Model):
    __tablename__ = "app_user"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    causes = db.relationship('Cause', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    contacts = db.relationship('UserContact', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    socials = db.relationship('UserSocials', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    donations = db.relationship('Donation', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    feedbacks = db.relationship('Feedback', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    volunteer_roles = db.relationship('Volunteer', backref='user', cascade="all, delete-orphan", passive_deletes=True)
    account_details = db.relationship('AccountDetails', backref='user', cascade="all, delete-orphan", passive_deletes=True)

    auth_id = db.Column(db.Integer, db.ForeignKey('auth_data.id', ondelete="CASCADE"), unique=True)
    auth = db.relationship("AuthData", backref="user", uselist=False, cascade="all, delete")


# ============================
#           CAUSE
# ============================
class Cause(db.Model):
    __tablename__ = 'cause'

    cause_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    logo = db.Column(db.String(255))
    email = db.Column(db.String(120))
    if_online = db.Column(db.Boolean, default=False)
    verified = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)

    ngo = db.relationship('NGO', uselist=False, backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    event = db.relationship('Event', uselist=False, backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    locations = db.relationship('Location', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    account_details = db.relationship('AccountDetails', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    feedbacks = db.relationship('Feedback', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    donations = db.relationship('Donation', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    volunteers = db.relationship('Volunteer', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    socials = db.relationship('CauseSocials', backref='cause', cascade="all, delete-orphan", passive_deletes=True)
    contacts = db.relationship('CauseContact', backref='cause', cascade="all, delete-orphan", passive_deletes=True)

    auth_id = db.Column(db.Integer, db.ForeignKey('auth_data.id', ondelete="CASCADE"), unique=True)
    auth = db.relationship("AuthData", backref="cause", uselist=False, cascade="all, delete")


# ============================
#            NGO
# ============================
class NGO(db.Model):
    __tablename__ = 'ngo'

    ngo_id = db.Column(db.Integer, primary_key=True)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), unique=True, nullable=False)
    year_est = db.Column(db.Integer)
    age = db.Column(db.Integer)


# ============================
#           EVENT
# ============================
class Event(db.Model):
    __tablename__ = 'event'

    event_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.ngo_id', ondelete="SET NULL"))


# ============================
#         LOCATION
# ============================
class Location(db.Model):
    __tablename__ = 'location'

    loc_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    contact_no = db.Column(db.String(50))

    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"))


# ============================
#     ACCOUNT DETAILS
# ============================
class AccountDetails(db.Model):
    __tablename__ = 'account_details'

    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(50), unique=True)
    acc_name = db.Column(db.String(100))

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=True)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=True)


# ============================
#         FEEDBACK
# ============================
class Feedback(db.Model):
    __tablename__ = 'feedback'

    feedback_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer)

    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)


# ============================
#         DONATION
# ============================
class Donation(db.Model):
    __tablename__ = 'donation'

    donation_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)


# ============================
#         VOLUNTEER
# ============================
class Volunteer(db.Model):
    __tablename__ = 'volunteer'

    volunteer_id = db.Column(db.Integer, primary_key=True)

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)


# ============================
#     USER CONTACT
# ============================
class UserContact(db.Model):
    __tablename__ = 'user_contact'

    contact_id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)


# ============================
#      USER SOCIALS
# ============================
class UserSocials(db.Model):
    __tablename__ = 'user_socials'

    social_id = db.Column(db.Integer, primary_key=True)
    social = db.Column(db.String(100))

    # FIXED HERE ↓↓↓
    user_id = db.Column(db.Integer, db.ForeignKey('app_user.user_id', ondelete="CASCADE"), nullable=False)


# ============================
#      CAUSE CONTACT
# ============================
class CauseContact(db.Model):
    __tablename__ = 'cause_contact'

    contact_id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))

    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)


# ============================
#      CAUSE SOCIALS
# ============================
class CauseSocials(db.Model):
    __tablename__ = 'cause_socials'

    social_id = db.Column(db.Integer, primary_key=True)
    social = db.Column(db.String(100))

    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id', ondelete="CASCADE"), nullable=False)