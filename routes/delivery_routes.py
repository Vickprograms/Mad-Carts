from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.delivery_controller import DeliveryController

delivery_bp = Blueprint("delivery", __name__, url_prefix="/deliveries")

@delivery_bp.route("/", methods=["POST"])
@jwt_required()
def create_delivery():
    return DeliveryController.create_delivery()

@delivery_bp.route("/", methods=["GET"])
@jwt_required()
def get_deliveries():
    return DeliveryController.list_deliveries()

@delivery_bp.route("/<delivery_id>", methods=["PATCH"])
@jwt_required()
def update_delivery(delivery_id):
    return DeliveryController.update_delivery(delivery_id)
