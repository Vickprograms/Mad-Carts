from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order, OrderItem, OrderSchema
from extensions import db

order_bp = Blueprint('order_bp', __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@order_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    result = orders_schema.dump(orders)
    return jsonify(result), 200


@order_bp.route('/single', methods=['POST'])
@jwt_required()
def get_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify(order_schema.dump(order)), 200


@order_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    total_amount = data.get('total_amount')
    order_items_data = data.get('order_items', [])

    if not total_amount or not order_items_data:
        return jsonify({"error": "Missing required fields"}), 400

    order = Order(user_id=user_id, total_amount=total_amount)
    db.session.add(order)
    db.session.commit()

    for item in order_items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify(order_schema.dump(order)), 201


@order_bp.route('/update', methods=['PATCH'])
@jwt_required()
def update_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    for key, value in data.items():
        if key != "id":
            setattr(order, key, value)

    db.session.commit()
    return jsonify(order_schema.dump(order)), 200


@order_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
        
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 204
