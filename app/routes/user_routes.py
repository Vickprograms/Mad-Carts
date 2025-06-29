from flask import Blueprint, request, jsonify
from app.controllers.user_controller import UserController
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem
from extensions import db
from werkzeug.security import generate_password_hash

user_bp = Blueprint("user", __name__, url_prefix="/users")

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    return UserController.get_me()


@user_bp.route("/", methods=["GET", "OPTIONS"])
@jwt_required()
def get_all_users():
    
    if request.method == "OPTIONS":
        return '', 200
        
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@user_bp.route("/", methods=["POST", "OPTIONS"])
@jwt_required()
def create_user():
    
    if request.method == "OPTIONS":
        return '', 200
        
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone_no = data.get("phone_no")
    role = data.get("role", "customer").lower()

    if role not in ["customer", "driver", "admin"]:
        return jsonify({"error": "Invalid role"}), 400

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username,
        email=email,
        phone_no=phone_no,
        password=hashed_password,
        is_driver=(role == "driver"),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User created successfully",
        "user": new_user.serialize()
    }), 201

@user_bp.route("/<user_id>", methods=["PUT", "OPTIONS"])
@jwt_required()
def update_user(user_id):
    
    if request.method == "OPTIONS":
        return '', 200
        
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user or current_user.role != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.get_json()
    
    if "username" in data:
        # Check if username is already taken by another user
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Username already taken"}), 409
        user.username = data["username"]
    
    if "email" in data:
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Email already taken"}), 409
        user.email = data["email"]
    
    if "phone_no" in data:
        user.phone_no = data["phone_no"]
    
    if "role" in data:
        role = data["role"].lower()
        if role not in ["customer", "driver", "admin"]:
            return jsonify({"error": "Invalid role"}), 400
        user.role = role
        user.is_driver = (role == "driver")
    
    if "password" in data:
        user.password = generate_password_hash(data["password"])
    
    db.session.commit()
    
    return jsonify({
        "message": "User updated successfully",
        "user": user.serialize()
    }), 200

@user_bp.route("/<user_id>", methods=["DELETE", "OPTIONS"])
@jwt_required()
def delete_user(user_id):
    
    if request.method == "OPTIONS":
        return '', 200
        
    try:
        current_user_id = get_jwt_identity()
        print(f"🔍 DEBUG: Current user ID: {current_user_id}")
        
        current_user = User.query.get(current_user_id)
        print(f"🔍 DEBUG: Current user: {current_user}")
        
        if not current_user or current_user.role != 'admin':
            print(f"🔍 DEBUG: Not admin - role: {current_user.role if current_user else 'None'}")
            return jsonify({"error": "Admin access required"}), 403
        
        # Prevent admin from deleting themselves
        if str(current_user.id) == user_id:
            print(f" DEBUG: Admin trying to delete themselves")
            return jsonify({"error": "Cannot delete your own account"}), 400
        
        user = User.query.get(user_id)
        print(f" DEBUG: User to delete: {user}")
        
        if not user:
            print(f" DEBUG: User not found")
            return jsonify({"error": "User not found"}), 404
        
        print(f" DEBUG: Attempting to delete user {user_id}")
        
        print(f" DEBUG: Cleaning up related data for user {user_id}")
        
        # Delete cart items and carts
        carts = Cart.query.filter_by(user_id=user.id).all()
        print(f" DEBUG: Found {len(carts)} carts to delete")
        for cart in carts:
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            print(f" DEBUG: Deleting {len(cart_items)} cart items from cart {cart.id}")
            for cart_item in cart_items:
                db.session.delete(cart_item)
            db.session.delete(cart)
        

        orders = Order.query.filter_by(user_id=user.id).all()
        print(f" DEBUG: Found {len(orders)} orders to delete")
        for order in orders:
            order_items = OrderItem.query.filter_by(order_id=order.id).all()
            print(f" DEBUG: Deleting {len(order_items)} order items from order {order.id}")
            for order_item in order_items:
                db.session.delete(order_item)
            db.session.delete(order)
        
        print(f" DEBUG: Deleting user {user_id}")
        db.session.delete(user)
        db.session.commit()
        
        print(f" DEBUG: User deleted successfully")
        return jsonify({"message": "User deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f" ERROR: Error deleting user {user_id}: {str(e)}")
        return jsonify({"error": "Failed to delete user. User may have related data."}), 500
