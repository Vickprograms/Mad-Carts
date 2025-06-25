from flask import request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token

class AuthController:
    @staticmethod
    def register():
        data = request.get_json()

        if User.query.filter_by(email=data.get("email")).first():
            return jsonify({"error": "Email already exists"}), 400

        if User.query.filter_by(username=data.get("username")).first():
            return jsonify({"error": "Username already taken"}), 400

        role = data.get("role", "customer").lower()
        if role not in ["customer", "driver", "admin"]:
            return jsonify({"error": "Invalid role"}), 400

        user = User(
            email=data["email"],
            username=data["username"],
            phone_no=data.get("phone_no"),
            role=role
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": f"{role.capitalize()} registered successfully"}), 201

    @staticmethod
    def login():
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not user.check_password(data.get("password")):
            return jsonify({"error": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token})