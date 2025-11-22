# backend/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from backend import db
from werkzeug.security import check_password_hash
from datetime import datetime

from backend.models import (
    AuthData, User, Cause, NGO, Event,
    AccountDetails, Donation, Feedback, Volunteer,
    UserContact, UserSocials, CauseContact, CauseSocials,
    Location, generate_next_cause_id
)

main = Blueprint("main", __name__)

# ------------------------------------------------------------
# HELPER: ENSURE ADMIN EXISTS
# ------------------------------------------------------------
def create_admin_if_missing():
    admin = AuthData.query.filter_by(id=1).first()
    if not admin:
        admin = AuthData(
            id=1,
            name="Admin",
            role="admin",
            verified=True
        )
        admin.set_password("ADMIN@123")
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

    # Create AuthData (always unverified)
    auth = AuthData(name=name, role=role, verified=False)
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

        return jsonify({
            "message": "User created, awaiting admin verification.",
            "auth_id": auth.id,
            "user_id": user.user_id
        }), 201

    # ---------------- NGO / EVENT ----------------
    owner_user_id = data.get("user_id")
    if not owner_user_id:
        return jsonify({"error": "NGO/Event requires user_id (owner)"}), 400

    owner = User.query.get(owner_user_id)
    if not owner:
        return jsonify({"error": "Owner user does not exist"}), 404

    if not owner.verified:
        return jsonify({"error": "Owner user must be verified first"}), 403

    # Create cause
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

    # Subtype table
    if role == "ngo":
        subtype = NGO(
            cause_id=cause_id,
            year_est=data.get("year_est"),
            age=data.get("age")
        )
    else:
        subtype = Event(
            cause_id=cause_id,
            capacity=data.get("capacity"),
            date=data.get("date"),
            time=data.get("time"),
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
# LOGIN (auth only)
# ------------------------------------------------------------
@main.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    auth = AuthData.query.filter_by(name=data["name"]).first()
    if not auth:
        return jsonify({"error": "Invalid credentials"}), 401

    if not auth.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    if not auth.verified:
        return jsonify({"error": "Account not verified by admin"}), 403

    token = create_access_token(identity=auth.id)

    return jsonify({
        "token": token,
        "auth_id": auth.id,
        "role": auth.role,
        "name": auth.name
    })


# ------------------------------------------------------------
# ADMIN ACCESS CHECKER
# ------------------------------------------------------------
def require_admin():
    auth_id = get_jwt_identity()
    auth = AuthData.query.get(auth_id)
    return (auth and auth.role == "admin")


# ------------------------------------------------------------
# ADMIN: GET LISTS
# ------------------------------------------------------------
@main.route("/api/admin/users", methods=["GET"])
@jwt_required()
def admin_get_users():
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

    users = User.query.all()
    result = []
    for u in users:
        auth = AuthData.query.get(u.auth_id)
        result.append({
            "user_id": u.user_id,
            "auth_id": u.auth_id,
            "name": u.name,
            "verified": u.verified,
            "role": auth.role if auth else "unknown"
        })

    return jsonify(result)


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
        return jsonify({"error": "Auth not found"}), 404

    auth.verified = True
    db.session.commit()

    # mirror to user/cause
    if auth.role == "user":
        user = User.query.filter_by(auth_id=auth.id).first()
        if user:
            user.verified = True
            db.session.commit()

    else:
        cause = Cause.query.filter_by(name=auth.name).first()
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
        return jsonify({"error": "Auth not found"}), 404

    auth.verified = False
    db.session.commit()

    # mirror to user/cause
    if auth.role == "user":
        user = User.query.filter_by(auth_id=auth.id).first()
        if user:
            user.verified = False
            db.session.commit()

    else:
        cause = Cause.query.filter_by(name=auth.name).first()
        if cause:
            cause.verified = False
            db.session.commit()

    return jsonify({"message": "Unverified"})


# ------------------------------------------------------------
# ADMIN DELETE USER (cascades)
# ------------------------------------------------------------
def delete_user_cascade(user_id):
    user = User.query.get(user_id)
    if not user:
        return False

    # Delete causes owned by user
    causes = Cause.query.filter_by(user_id=user_id).all()
    for cause in causes:
        delete_cause_cascade(cause.cause_id)

    # User contacts + socials
    UserContact.query.filter_by(user_id=user_id).delete()
    UserSocials.query.filter_by(user_id=user_id).delete()

    # Remove user
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
        return jsonify({"error": "User not found"}), 404

    delete_user_cascade(user_id)

    # Delete auth
    auth = AuthData.query.get(user.auth_id)
    if auth:
        db.session.delete(auth)
        db.session.commit()

    return jsonify({"message": "User deleted"})


# ------------------------------------------------------------
# ADMIN DELETE CAUSE (cascades)
# ------------------------------------------------------------
def delete_cause_cascade(cause_id):
    cause = Cause.query.get(cause_id)
    if not cause:
        return False

    # Subtype tables
    NGO.query.filter_by(cause_id=cause_id).delete()
    Event.query.filter_by(cause_id=cause_id).delete()

    # Linked tables
    Location.query.filter_by(cause_id=cause_id).delete()
    CauseContact.query.filter_by(cause_id=cause_id).delete()
    CauseSocials.query.filter_by(cause_id=cause_id).delete()
    Donation.query.filter_by(cause_id=cause_id).delete()
    Feedback.query.filter_by(cause_id=cause_id).delete()
    Volunteer.query.filter_by(cause_id=cause_id).delete()

    db.session.delete(cause)
    db.session.commit()
    return True


@main.route("/api/admin/delete/cause/<int:cause_id>", methods=["DELETE"])
@jwt_required()
def admin_delete_cause(cause_id):
    if not require_admin():
        return jsonify({"error": "Admin only"}), 403

    cause = Cause.query.get(cause_id)
    if not cause:
        return jsonify({"error": "Cause not found"}), 404

    delete_cause_cascade(cause_id)

    # Also delete matching AuthData
    auth = AuthData.query.filter_by(name=cause.name).first()
    if auth:
        db.session.delete(auth)
        db.session.commit()

    return jsonify({"message": "Cause deleted"})