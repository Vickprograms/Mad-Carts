from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from extensions import db
from app.models.cart import Cart, CartItem, CartSchema, CartItemSchema

cart_bp = Blueprint("cart_bp", __name__)
cart_schema = CartSchema()
cart_item_schema = CartItemSchema()

# 1. Get current user's cart
@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"message": "Cart is empty"}), 200
    return cart_schema.dump(cart), 200

# 2. Create a new cart
@cart_bp.route("/", methods=["POST"])
@jwt_required()
def create_cart():
    user_id = get_jwt_identity()
    existing = Cart.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({"error": "Cart already exists"}), 400

    cart = Cart(user_id=user_id)
    db.session.add(cart)
    db.session.commit()
    return cart_schema.dump(cart), 201

# 3. Add an item to the user's cart
@cart_bp.route("/add-item", methods=["POST"])
@jwt_required()
def add_item():
    user_id = get_jwt_identity()
    data = request.get_json(force=True)

    try:
        validated_item = cart_item_schema.load(data)
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 422

    product_id = validated_item["product_id"]
    price = validated_item["price"]
    quantity = validated_item["quantity"]

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            price=price,
            quantity=quantity
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({"message": "Item added"}), 200

# 4. Update quantity of an item
@cart_bp.route("/update-item", methods=["PATCH"])
@jwt_required()
def update_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    cart = Cart.query.filter_by(user_id=user_id).first()
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    item.quantity = quantity
    db.session.commit()
    return jsonify({"message": "Item updated"}), 200

# 5. Remove item from cart
@cart_bp.route("/remove-item", methods=["DELETE"])
@jwt_required()
def remove_item():
    user_id = get_jwt_identity()
    product_id = request.args.get("product_id")

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"}), 200

# 6. Delete whole cart
@cart_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"error": "No cart to delete"}), 404

    db.session.delete(cart)
    db.session.commit()
    return jsonify({"message": "Cart deleted"}), 204

@cart_bp.route("/test-add-item", methods=["POST"])
def test_add_item():
    test_user_id = "some-valid-uuid-user-id"
    test_data = {
        "product_id": "2ba575bd-a755-44b7-8d6f-37177eb93558",
        "price": 2000,
        "quantity": 1
    }

    from marshmallow import ValidationError
    try:
        validated_item = cart_item_schema.load(test_data)
    except ValidationError as ve:
        return jsonify({"error": ve.messages}), 422

    cart = Cart.query.filter_by(user_id=test_user_id).first()
    if not cart:
        cart = Cart(user_id=test_user_id)
        db.session.add(cart)
        db.session.flush()

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=validated_item["product_id"]).first()
    if item:
        item.quantity += validated_item["quantity"]
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=validated_item["product_id"],
            price=validated_item["price"],
            quantity=validated_item["quantity"]
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({"message": "Test item added successfully"}), 200
