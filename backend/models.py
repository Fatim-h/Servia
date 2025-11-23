from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ---------------- AUTH ----------------
class AuthData(db.Model):
    __tablename__ = 'auth_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # user, ngo, event, admin
    password_hash = db.Column(db.String(255), nullable=False)

    verified = db.Column(db.Boolean, default=False)

    # FK that links to User OR Cause record
    fk_id = db.Column(db.Integer, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ---------------- USER ----------------
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer)
    verified = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    contacts = db.relationship('UserContact', backref='user', lazy=True)
    socials = db.relationship('UserSocials', backref='user', lazy=True)
    donations = db.relationship('Donation', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    volunteer_roles = db.relationship('Volunteer', backref='user', lazy=True)
    account_details = db.relationship('AccountDetails', backref='user', lazy=True)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth_data.id'), unique=True)
    auth = db.relationship("AuthData", backref="user", uselist=False)


# ---------------- CAUSE ----------------
class Cause(db.Model):
    __tablename__ = 'cause'
    cause_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    if_online = db.Column(db.Boolean, default=False)
    logo = db.Column(db.String(255))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship("User", backref="causes")

    ngo = db.relationship('NGO', uselist=False, backref='cause')
    event = db.relationship('Event', uselist=False, backref='cause')
    locations = db.relationship('Location', backref='cause', lazy=True)
    account_details = db.relationship('AccountDetails', backref='cause', lazy=True)
    feedbacks = db.relationship('Feedback', backref='cause', lazy=True)
    donations = db.relationship('Donation', backref='cause', lazy=True)
    volunteers = db.relationship('Volunteer', backref='cause', lazy=True)
    socials = db.relationship('CauseSocials', backref='cause', lazy=True)
    contacts = db.relationship('CauseContact', backref='cause', lazy=True)
    auth_id = db.Column(db.Integer, db.ForeignKey('auth_data.id'), unique=True)
    auth = db.relationship("AuthData", backref="cause", uselist=False)
    verified = db.Column(db.Boolean, default=False)

# ---------------- NGO ----------------
class NGO(db.Model):
    __tablename__ = 'ngo'
    ngo_id = db.Column(db.Integer, primary_key=True)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'), unique=True)
    year_est = db.Column(db.Integer)
    age = db.Column(db.Integer)


# ---------------- EVENT ----------------
class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.ngo_id'))


# ---------------- LOCATION ----------------
class Location(db.Model):
    __tablename__ = 'location'
    loc_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    city = db.Column(db.String(100))
    contact_no = db.Column(db.String(50))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))
    address = db.Column(db.String(255))


# ---------------- ACCOUNT DETAILS ----------------
class AccountDetails(db.Model):
    __tablename__ = 'account_details'
    id = db.Column(db.Integer, primary_key=True)
    iban = db.Column(db.String(50), unique=True)
    acc_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))


# ---------------- FEEDBACK ----------------
class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    rating = db.Column(db.Integer)
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


# ---------------- DONATION ----------------
class Donation(db.Model):
    __tablename__ = 'donation'
    donation_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))


# ---------------- VOLUNTEER ----------------
class Volunteer(db.Model):
    __tablename__ = 'volunteer'
    volunteer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))


# ---------------- USER CONTACT / SOCIAL ----------------
class UserContact(db.Model):
    __tablename__ = 'user_contact'
    contact_id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


class UserSocials(db.Model):
    __tablename__ = 'user_socials'
    social_id = db.Column(db.Integer, primary_key=True)
    social = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))


# ---------------- CAUSE CONTACT / SOCIAL ----------------
class CauseContact(db.Model):
    __tablename__ = 'cause_contact'
    contact_id = db.Column(db.Integer, primary_key=True)
    contact = db.Column(db.String(100))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))


class CauseSocials(db.Model):
    __tablename__ = 'cause_socials'
    social_id = db.Column(db.Integer, primary_key=True)
    social = db.Column(db.String(100))
    cause_id = db.Column(db.Integer, db.ForeignKey('cause.cause_id'))


# ---------------- HELPER ----------------
def generate_next_cause_id(is_ngo: bool):
    """
    Generate next CauseID:
      - Even for NGO
      - Odd for Event
    """
    if is_ngo:
        max_id = db.session.query(db.func.max(Cause.cause_id))\
                 .filter(Cause.cause_id % 2 == 0).scalar()
        return 2 if max_id is None else max_id + 2
    else:
        max_id = db.session.query(db.func.max(Cause.cause_id))\
                 .filter(Cause.cause_id % 2 == 1).scalar()
        return 1 if max_id is None else max_id + 2