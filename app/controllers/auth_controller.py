from flask import request, jsonify
from app.models.user import User
from extensions import db
from flask_jwt_extended import create_access_token


class AuthController:
    @staticmethod
    def register():
        data = request.get_json()

        # Ensure required fields are present
        required_fields = ["email", "username", "password"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field.capitalize()} is required"}), 400

        # Check if email or username already exists
        if User.query.filter_by(email=data.get("email")).first():
            return jsonify({"error": "Email already exists"}), 400
        if User.query.filter_by(username=data.get("username")).first():
            return jsonify({"error": "Username already taken"}), 400

        # Validate role
        role = data.get("role", "customer").lower()
        if role not in ["customer", "driver", "admin"]:
            return jsonify({"error": "Invalid role"}), 400

        # Create new user
        user = User(
            email=data["email"],
            username=data["username"],
            phone_no=data.get("phone_no"),
            role=role
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()

        # Generate JWT with full identity including role
        access_token = create_access_token(identity={
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

        return jsonify({
            "message": f"{role.capitalize()} registered successfully",
            "access_token": access_token
        }), 201

    @staticmethod
    def login():
        data = request.get_json()

        # Check credentials
        user = User.query.filter_by(email=data.get("email")).first()
        if not user or not user.check_password(data.get("password")):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT with user info
        access_token = create_access_token(identity={
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

        return jsonify({
            "access_token": access_token
        }), 200
