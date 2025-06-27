from flask import Blueprint, request, jsonify
from extensions import db
from app.models.cart import Cart, CartItem, CartSchema, CartItemSchema

cart_bp = Blueprint('cart_bp', __name__)

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)
cart_item_schema = CartItemSchema()
cart_items_schema = CartItemSchema(many=True)


@cart_bp.route('/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return carts_schema.dump(carts), 200

@cart_bp.route('/carts/<int:id>', methods=['GET'])
def get_cart(id):
    cart = Cart.query.get_or_404(id)
    return cart_schema.dump(cart), 200


@cart_bp.route('/carts', methods=['POST'])
def create_cart():
    data = request.get_json()
    
    
    errors = cart_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    cart = Cart(user_id=data['user_id'])

    
    cart_items_data = data.get('cart_items', [])
    for item_data in cart_items_data:
        item_errors = cart_item_schema.validate(item_data)
        if item_errors:
            return jsonify(item_errors), 400
        
        item = CartItem(
            product_id=item_data['product_id'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        cart.cart_items.append(item)

    db.session.add(cart)
    db.session.commit()

    return cart_schema.dump(cart), 201
    
@cart_bp.route('/carts/<int:id>', methods=['PATCH'])
def update_cart(id):
    cart = Cart.query.get_or_404(id)
    data = request.get_json()

    if 'user_id' in data:
        cart.user_id = data['user_id']

    db.session.commit()
    return cart_schema.dump(cart), 200

@cart_bp.route('/carts/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get_or_404(id)
    db.session.delete(cart)
    db.session.commit()
    return jsonify({"message": f"Cart {id} deleted."}), 204
