# backend/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from backend import db
from werkzeug.security import check_password_hash
from datetime import datetime, date, time

from backend.models import (
    AuthData, User, Cause, NGO, Event,
    AccountDetails, Donation, Feedback, Volunteer,
    UserContact, UserSocials, CauseContact, CauseSocials,
    Location, generate_next_cause_id
)
from backend.models import *

main = Blueprint("main", __name__)

# ------------------------------------------------------------
# HELPER: CREATE DEFAULT ADMIN (ID=1)
# ------------------------------------------------------------
def create_admin_if_missing():
    admin = AuthData.query.filter_by(id=1).first()
    if not admin:
        admin = AuthData(
            id=0,
            name="admin",
            role="admin",
            verified=True,
            fk_id=None
        )
        admin.set_password("admin")
        db.session.add(admin)
        db.session.commit()


# ------------------------------------------------------------
# REGISTER (SIGNUP)
# ------------------------------------------------------------
@main.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    required = ["name", "password", "role"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing fields"}), 400

    role = data["role"]
    name = data["name"]
    password = data["password"]

    if role not in ["user", "ngo", "event"]:
        return jsonify({"error": "Role must be user, ngo, or event"}), 400

    # Create AuthData
    auth = AuthData(
        name=name,
        role=role,
        verified=False
    )
    auth.set_password(password)
    db.session.add(auth)
    db.session.commit()

    # ---------------- USER ----------------
    if role == "user":
        user = User(
            auth_id=auth.id,
            name=name,
            verified=False
        )
        db.session.add(user)
        db.session.commit()

        auth.fk_id = user.user_id
        db.session.commit()

        return jsonify({
            "message": "User created, awaiting admin verification.",
            "auth_id": auth.id,
            "user_id": user.user_id
        }), 201

    # ---------------- NGO / EVENT ----------------
    owner_user_id = data.get("user_id")
    if not owner_user_id:
        return jsonify({"error": "NGO/Event requires owner user_id"}), 400

    owner = User.query.get(owner_user_id)
    if not owner:
        return jsonify({"error": "Owner user not found"}), 404

    if not owner.verified:
        return jsonify({"error": "Owner must be admin-verified"}), 403

    cause_id = generate_next_cause_id(is_ngo=(role == "ngo"))

    cause = Cause(
        cause_id=cause_id,
        name=name,
        email=data.get("email"),
        description=data.get("description"),
        if_online=data.get("if_online", False),
        logo=data.get("logo"),
        user_id=owner_user_id,
        verified=False
    )
    db.session.add(cause)
    db.session.commit()

    # Link Auth to Cause
    auth.fk_id = cause.cause_id
    db.session.commit()

    # Subtype
    if role == "ngo":
        subtype = NGO(
            cause_id=cause_id,
            year_est=data.get("year_est"),
            age=data.get("age")
        )
    else:
        # safe event parsing
        event_date = None
        event_time = None

        if data.get("date"):
            event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()

        if data.get("time"):
            event_time = datetime.strptime(data["time"], "%H:%M").time()

        subtype = Event(
            cause_id=cause_id,
            capacity=data.get("capacity"),
            date=event_date,
            time=event_time,
            ngo_id=data.get("ngo_id")
        )

    db.session.add(subtype)
    db.session.commit()

    return jsonify({
        "message": f"{role} created, awaiting admin verification.",
        "auth_id": auth.id,
        "cause_id": cause_id
    }), 201


# ------------------------------------------------------------
# LOGIN (use name, but email recommended later)
# ------------------------------------------------------------
@main.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    auth = AuthData.query.filter_by(name=data["name"]).first()
    if not auth or not auth.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    if not auth.verified:
        return jsonify({"error": "Account not verified"}), 403

    # JWT with custom claims
    token = create_access_token(identity={"id": auth.id, "role": auth.role})

    return jsonify({
        "token": token,
        "auth_id": auth.id,
        "role": auth.role,
        "name": auth.name
    })


# ------------------------------------------------------------
# ADMIN CHECK
# ------------------------------------------------------------
def require_admin():
    ident = get_jwt_identity()
    return ident and ident.get("role") == "admin"


# ------------------------------------------------------------
# ADMIN: GET USERS / CAUSES
# ------------------------------------------------------------
@main.route("/api/admin/users", methods=["GET"])
@jwt_required()
def admin_get_users():
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "user_id": u.user_id,
            "auth_id": u.auth_id,
            "name": u.name,
            "verified": u.verified
        })
    return jsonify(result)
#homepage causes
@main.route("/api/causes", methods=["GET"])
def get_all_causes():
    causes = Cause.query.filter_by(verified=True).all()
    result = []

    for c in causes:
        # Determine subtype
        if c.ngo:
            subtype = "NGO"
        elif c.event:
            subtype = "Event"
        else:
            subtype = "Unknown"

        # Collect common fields
        cause_data = {
            "cause_id": c.cause_id,
            "name": c.name,
            "description": c.description,
            "logo": c.logo,
            "type": subtype,
            "latitude": c.locations[0].latitude if c.locations else None,
            "longitude": c.locations[0].longitude if c.locations else None,
            "contacts": [con.contact for con in c.contacts],
            "socials": [soc.social for soc in c.socials],
        }

        # Add subtype-specific fields
        if subtype == "NGO":
            cause_data.update({
                "year_est": c.ngo.year_est,
                "age": c.ngo.age
            })
        elif subtype == "Event":
            cause_data.update({
                "date": c.event.date.strftime("%Y-%m-%d") if c.event.date else None,
                "time": c.event.time.strftime("%H:%M") if c.event.time else None,
                "capacity": c.event.capacity
            })

        result.append(cause_data)

    return jsonify({"causes": result})

#admin causes
@main.route("/api/admin/causes", methods=["GET"])
@jwt_required()
def admin_get_causes():
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

    causes = Cause.query.all()
    result = []
    for c in causes:
        subtype = "NGO" if c.ngo else "Event"
        result.append({
            "cause_id": c.cause_id,
            "name": c.name,
            "verified": c.verified,
            "type": subtype
        })
    return jsonify(result)


# ------------------------------------------------------------
# ADMIN: VERIFY / UNVERIFY
# ------------------------------------------------------------
@main.route("/api/admin/verify/<int:auth_id>", methods=["PATCH"])
@jwt_required()
def admin_verify(auth_id):
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

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
@jwt_required()
def admin_unverify(auth_id):
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

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


# ------------------------------------------------------------
# CASCADE DELETIONS
# ------------------------------------------------------------
def delete_cause_cascade(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause:
        return False

    NGO.query.filter_by(cause_id=cause_id).delete()
    Event.query.filter_by(cause_id=cause_id).delete()

    Location.query.filter_by(cause_id=cause_id).delete()
    CauseContact.query.filter_by(cause_id=cause_id).delete()
    CauseSocials.query.filter_by(cause_id=cause_id).delete()
    Donation.query.filter_by(cause_id=cause_id).delete()
    Feedback.query.filter_by(cause_id=cause_id).delete()
    Volunteer.query.filter_by(cause_id=cause_id).delete()
    AccountDetails.query.filter_by(cause_id=cause_id).delete()

    db.session.delete(cause)
    db.session.commit()
    return True


def delete_user_cascade(user_id):
    user = User.query.get(user_id)
    if not user:
        return False

    causes = Cause.query.filter_by(user_id=user_id).all()
    for c in causes:
        delete_cause_cascade(c.cause_id)

    UserContact.query.filter_by(user_id=user_id).delete()
    UserSocials.query.filter_by(user_id=user_id).delete()
    AccountDetails.query.filter_by(user_id=user_id).delete()

    db.session.delete(user)
    db.session.commit()
    return True


@main.route("/api/admin/delete/user/<int:user_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_user(user_id):
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

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
@jwt_required()
def admin_delete_cause(cause_id):
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

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
# GET SINGLE CAUSE (for CausePage)
# ------------------------------------------------------------
@main.route("/api/causes/<int:cause_id>", methods=["GET"])
def get_cause(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause or not cause.verified:
        return jsonify({"error": "Cause not found"}), 404

    # Determine subtype
    subtype = "NGO" if cause.ngo else "Event"

    # Common cause info
    cause_data = {
        "cause_id": cause.cause_id,
        "name": cause.name,
        "description": cause.description,
        "logo": cause.logo,
        "type": subtype,
        "email": cause.email,
        "if_online": cause.if_online,
        "verified": cause.verified,
        "locations": [],
        "contacts": [],
        "socials": []
    }

    # Add subtype-specific fields
    if subtype == "NGO" and cause.ngo:
        cause_data.update({
            "year_est": cause.ngo.year_est,
            "age": cause.ngo.age
        })
    elif subtype == "Event" and cause.event:
        cause_data.update({
            "capacity": cause.event.capacity,
            "date": cause.event.date.strftime("%Y-%m-%d") if cause.event.date else None,
            "time": cause.event.time.strftime("%H:%M") if cause.event.time else None,
            "ngo_id": cause.event.ngo_id
        })

    # Add locations
    for loc in cause.locations:
        cause_data["locations"].append({
            "loc_id": loc.loc_id,
            "country": loc.country,
            "city": loc.city,
            "address": loc.address,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "contact_no": loc.contact_no
        })

    # Add contacts
    for contact in cause.contacts:
        cause_data["contacts"].append(contact.contact)

    # Add socials
    for social in cause.socials:
        cause_data["socials"].append(social.social)

    return jsonify(cause_data)
