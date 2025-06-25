from flask import Blueprint
from controllers.user_controller import UserController
from flask_jwt_extended import jwt_required

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    return UserController.get_me()
