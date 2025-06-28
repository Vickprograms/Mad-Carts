from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone_no = data.get("phone_no")
    role = data.get("role", "customer").lower()

    if role not in ["customer", "driver", "admin"]:
        return jsonify({"error": "Invalid role"}), 400

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        phone_no=phone_no,
        password=hashed_password,
        is_driver=(role == "driver"),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    # ✅ Use only user ID for identity
    access_token = create_access_token(identity=str(new_user.id))

    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "user": {
            "id": str(new_user.id),
            "username": new_user.username,
            "email": new_user.email,
            "role": new_user.role,
            "is_driver": new_user.is_driver
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # ✅ Use only user ID for identity
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_driver": user.is_driver
        }
    }), 200




@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user_id():
    """
    Return the current logged-in user's ID from the JWT token.
    """
    user_id = get_jwt_identity()
    return jsonify({"user_id": user_id}), 200