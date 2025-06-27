from flask import Blueprint, request, jsonify
from app.models.order import Order, OrderItem
from app.models.schemas import OrderSchema
from extensions import db

order_bp = Blueprint('order_bp', __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders)), 200


@order_bp.route('/orders/single', methods=['POST'])  #  custom route for single order by ID in body
def get_order():
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.get_or_404(order_id)
    return jsonify(order_schema.dump(order)), 200


@order_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    user_id = data.get('user_id')
    total_amount = data.get('total_amount')
    order_items_data = data.get('order_items', [])

    if not user_id or not total_amount or not order_items_data:
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


@order_bp.route('/orders/update', methods=['PATCH'])  #  update using body UUID
def update_order():
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.get_or_404(order_id)

    for key, value in data.items():
        if key != "id":
            setattr(order, key, value)

    db.session.commit()
    return jsonify(order_schema.dump(order)), 200


@order_bp.route('/orders/delete', methods=['DELETE'])  #  delete using body UUID
def delete_order():
    data = request.get_json()
    order_id = data.get('id')

    if not order_id:
        return jsonify({"error": "Missing order ID"}), 400

    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 204
