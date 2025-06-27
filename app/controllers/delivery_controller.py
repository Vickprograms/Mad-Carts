from flask import request, jsonify
from app.models.delivery import Delivery
from extensions import db
from flask_jwt_extended import jwt_required
import datetime

class DeliveryController:
    @staticmethod
    def create_delivery():
        data = request.get_json()

        delivery = Delivery(
            order_id=data["order_id"],
            driver_id=data.get("driver_id"),
            delivery_date=data.get("delivery_date"),
            delivery_notes=data.get("delivery_notes")
        )

        db.session.add(delivery)
        db.session.commit()
        return jsonify(delivery.serialize()), 201

    @staticmethod
    def list_deliveries():
        deliveries = Delivery.query.all()
        return jsonify([d.serialize() for d in deliveries]), 200

    @staticmethod
    def update_delivery(delivery_id):
        delivery = Delivery.query.get(delivery_id)
        if not delivery:
            return jsonify({"error": "Delivery not found"}), 404

        data = request.get_json()
        if "status" in data:
            delivery.status = data["status"]
        if "driver_id" in data:
            delivery.driver_id = data["driver_id"]
        if data.get("status") == "Delivered":
            delivery.delivered_at = datetime.datetime.utcnow()

        db.session.commit()
        return jsonify(delivery.serialize()), 200
