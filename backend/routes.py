# backend/routes.py
from flask import Blueprint, request, jsonify, session
from backend import db
from werkzeug.security import check_password_hash
from datetime import datetime
from functools import wraps

from backend.models import (
    AuthData, User, Cause, NGO, Event,
    AccountDetails, Donation, Feedback, Volunteer,
    UserContact, UserSocials, CauseContact, CauseSocials,
    Location
)

main = Blueprint("main", __name__)

# ------------------------------------------------------------
# HELPER: CREATE DEFAULT ADMIN (ID=0)
# ------------------------------------------------------------
def create_admin_if_missing():
    admin = AuthData.query.filter_by(id=0).first()
    if not admin:
        admin = AuthData(
            id=0,
            name="admin",
            role="admin",
            verified=True,
            fk_id=None
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

# -------------------- REGISTER --------------------
@main.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    required_fields = ["name", "password", "role", "email"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"]
    password = data["password"]
    role = data["role"]
    email = data["email"]

    if role not in ["user", "ngo", "event"]:
        return jsonify({"error": "Invalid role"}), 400

    # Check duplicates
    if AuthData.query.filter_by(name=name).first() or User.query.filter_by(email=email).first():
        return jsonify({"error": "User/email already exists"}), 400

    auth = AuthData(name=name, role=role, verified=False)
    auth.set_password(password)
    db.session.add(auth)
    db.session.commit()

    if role == "user":
        user = User(name=name, email=email, verified=False, auth_id=auth.id)
        db.session.add(user)
        db.session.commit()
        auth.fk_id = user.user_id
        db.session.commit()
        return jsonify({"message": "User created, awaiting admin verification.", "auth_id": auth.id, "user_id": user.user_id}), 201

    # NGO / Event
    owner_user_id = data.get("owner_user_id")
    if not owner_user_id:
        return jsonify({"error": "NGO/Event requires owner_user_id"}), 400
    owner = User.query.get(owner_user_id)
    if not owner or not owner.verified:
        return jsonify({"error": "Owner must be admin-verified"}), 403

    cause = Cause(
        name=name,
        description=data.get("description"),
        email=email,
        if_online=data.get("if_online", False),
        logo=data.get("logo"),
        user_id=owner_user_id,
        verified=False,
        auth_id=auth.id
    )
    db.session.add(cause)
    db.session.commit()
    auth.fk_id = cause.cause_id
    db.session.commit()

    if role == "ngo":
        ngo = NGO(cause_id=cause.cause_id, year_est=data.get("year_est"), age=data.get("age"))
        db.session.add(ngo)
        db.session.commit()
    elif role == "event":
        event_date = datetime.strptime(data["date"], "%Y-%m-%d").date() if data.get("date") else None
        event_time = datetime.strptime(data["time"], "%H:%M").time() if data.get("time") else None
        event = Event(cause_id=cause.cause_id, capacity=data.get("capacity"), date=event_date, time=event_time, ngo_id=data.get("ngo_id"))
        db.session.add(event)
        db.session.commit()

    return jsonify({"message": f"{role.capitalize()} created, awaiting admin verification.", "auth_id": auth.id, "cause_id": cause.cause_id}), 201

# -------------------- LOGIN --------------------
@main.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    password = data.get("password")

    if not name or not password:
        return jsonify({"error": "Name and password required"}), 400

    auth = AuthData.query.filter_by(name=name).first()
    if not auth or not auth.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Set session
    session["user"] = {"id": auth.id, "role": auth.role, "name": auth.name}
    return jsonify({"auth_id": auth.id, "role": auth.role, "name": auth.name}), 200

# -------------------- LOGOUT --------------------
@main.route("/api/auth/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out"}), 200

# -------------------- CURRENT USER --------------------
@main.route("/api/auth/user", methods=["GET"])
def get_current_user():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify(user), 200

# ------------------------------------------------------------
# ADMIN CHECK DECORATOR
# ------------------------------------------------------------
def require_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "admin":
            return jsonify({"error": "Admin only"}), 403
        return f(*args, **kwargs)
    return wrapper

# ------------------------------------------------------------
# ADMIN ROUTES
# ------------------------------------------------------------
@main.route("/api/admin/users", methods=["GET"])
@require_admin
def admin_get_users():
    users = User.query.all()
    return jsonify([{
        "user_id": u.user_id,
        "auth_id": u.auth_id,
        "name": u.name,
        "verified": u.verified
    } for u in users])

@main.route("/api/admin/causes", methods=["GET"])
@require_admin
def admin_get_causes():
    causes = Cause.query.all()
    result = []
    for c in causes:
        subtype = "NGO" if c.ngo else "Event" if c.event else "Unknown"
        result.append({
            "cause_id": c.cause_id,
            "name": c.name,
            "verified": c.verified,
            "type": subtype
        })
    return jsonify(result)

# -------------------- VERIFY / UNVERIFY --------------------
@main.route("/api/admin/verify/<int:auth_id>", methods=["PATCH"])
@require_admin
def admin_verify(auth_id):
    auth = AuthData.query.get(auth_id)
    if not auth:
        return jsonify({"error": "Not found"}), 404

    auth.verified = True
    if auth.role == "user":
        user = User.query.get(auth.fk_id)
        if user:
            user.verified = True
    else:
        cause = Cause.query.get(auth.fk_id)
        if cause:
            cause.verified = True

    db.session.commit()
    return jsonify({"message": "Verified"})

@main.route("/api/admin/unverify/<int:auth_id>", methods=["PATCH"])
@require_admin
def admin_unverify(auth_id):
    auth = AuthData.query.get(auth_id)
    if not auth:
        return jsonify({"error": "Not found"}), 404

    auth.verified = False
    if auth.role == "user":
        user = User.query.get(auth.fk_id)
        if user:
            user.verified = False
    else:
        cause = Cause.query.get(auth.fk_id)
        if cause:
            cause.verified = False

    db.session.commit()
    return jsonify({"message": "Unverified"})

# -------------------- CASCADE DELETE --------------------
def delete_cause_cascade(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause:
        return False
    db.session.delete(cause)
    db.session.commit()
    return True

def delete_user_cascade(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

@main.route("/api/admin/delete/user/<int:user_id>", methods=["DELETE"])
@require_admin
def admin_delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404

    auth = AuthData.query.get(user.auth_id)
    delete_user_cascade(user_id)

    if auth:
        db.session.delete(auth)
        db.session.commit()

    return jsonify({"message": "User deleted"})

@main.route("/api/admin/delete/cause/<int:cause_id>", methods=["DELETE"])
@require_admin
def admin_delete_cause(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause:
        return jsonify({"error": "Not found"}), 404

    auth = AuthData.query.filter_by(fk_id=cause_id).first()
    delete_cause_cascade(cause_id)

    if auth:
        db.session.delete(auth)
        db.session.commit()

    return jsonify({"message": "Cause deleted"})

# ------------------------------------------------------------
# GET ALL CAUSES (for homepage)
# ------------------------------------------------------------
@main.route("/api/causes", methods=["GET"])
def get_all_causes():
    causes = Cause.query.filter_by(verified=True).all()
    result = []

    for c in causes:
        subtype = "NGO" if c.ngo else "Event" if c.event else "Unknown"
        cause_data = {
            "cause_id": c.cause_id,
            "name": c.name,
            "description": c.description,
            "logo": c.logo,
            "type": subtype,
            "contacts": [con.contact for con in c.contacts],
            "socials": [soc.social for soc in c.socials],
            "latitude": c.locations[0].latitude if c.locations else None,
            "longitude": c.locations[0].longitude if c.locations else None
        }
        if subtype == "NGO" and c.ngo:
            cause_data.update({"year_est": c.ngo.year_est, "age": c.ngo.age})
        elif subtype == "Event" and c.event:
            cause_data.update({
                "date": c.event.date.strftime("%Y-%m-%d") if c.event.date else None,
                "time": c.event.time.strftime("%H:%M") if c.event.time else None,
                "capacity": c.event.capacity
            })

        result.append(cause_data)

    return jsonify({"causes": result})

# ------------------------------------------------------------
# GET SINGLE CAUSE (for CausePage)
# ------------------------------------------------------------
@main.route("/api/causes/<int:cause_id>", methods=["GET"])
def get_cause(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause or not cause.verified:
        return jsonify({"error": "Cause not found"}), 404

    subtype = "NGO" if cause.ngo else "Event" if cause.event else "Unknown"

    cause_data = {
        "cause_id": cause.cause_id,
        "name": cause.name,
        "description": cause.description,
        "logo": cause.logo,
        "type": subtype,
        "email": cause.email,
        "if_online": cause.if_online,
        "verified": cause.verified,
        "locations": [{
            "loc_id": loc.loc_id,
            "country": loc.country,
            "city": loc.city,
            "address": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "contact_no": loc.contact_no
        } for loc in cause.locations] or [],
        "contacts": [c.contact for c in cause.contacts],
        "socials": [s.social for s in cause.socials]
    }

    if subtype == "NGO" and cause.ngo:
        cause_data.update({"year_est": cause.ngo.year_est, "age": cause.ngo.age})
    elif subtype == "Event" and cause.event:
        cause_data.update({
            "capacity": cause.event.capacity,
            "date": cause.event.date.strftime("%Y-%m-%d") if cause.event.date else None,
            "time": cause.event.time.strftime("%H:%M") if cause.event.time else None,
            "ngo_id": cause.event.ngo_id
        })

    return jsonify(cause_data)