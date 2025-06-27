from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

class UserController:
    @staticmethod
    def get_me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user.serialize())