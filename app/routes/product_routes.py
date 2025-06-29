from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.services.product_service import ProductService
from app.controllers.product_controller import (
    create_product_controller,
    get_all_products_controller,
    get_product_controller,
    update_product_controller,
    delete_product_controller
)
from extensions import db

product_bp = Blueprint('product', __name__)

product_service = ProductService()

def require_admin():
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return False
    return True

@product_bp.route('/create', methods=['POST', 'OPTIONS'])
@jwt_required()
def create_product():
    if request.method == "OPTIONS":
        return '', 200
    
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        return create_product_controller()
        
    except Exception as e:
        return jsonify({"error": "Failed to create product"}), 500

@product_bp.route('/products', methods=['GET'])
def get_products():
    return get_all_products_controller()

@product_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    return get_product_controller(product_id)

@product_bp.route('/<product_id>', methods=['PATCH', 'OPTIONS'])
@jwt_required()
def update_product(product_id):
    if request.method == "OPTIONS":
        return '', 200
    
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        return update_product_controller(product_id)
        
    except Exception as e:
        return jsonify({"error": "Failed to update product"}), 500

@product_bp.route('/<product_id>', methods=['DELETE', 'OPTIONS'])
@jwt_required()
def delete_product(product_id):
    if request.method == "OPTIONS":
        return '', 200
    
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        return delete_product_controller(product_id)
        
    except Exception as e:
        return jsonify({"error": "Failed to delete product"}), 500

@product_bp.route('/category', methods=['GET'])
def get_products_by_category():
    category = request.args.get('q')
    if not category:
        return {"error": "Missing category"}, 400
    products = product_service.get_products_by_category(category)
    return jsonify(products)

@product_bp.route('/autocomplete', methods=['GET'])
def search_products():
    term = request.args.get('term', '')
    results = product_service.search_products(term)
    return jsonify(results)

@product_bp.route('/filter', methods=['GET'])
def filter_products():
    filters = request.args.to_dict()
    filtered = product_service.filter_products(filters)
    return jsonify(filtered)

@product_bp.route('/sort', methods=['GET'])
def sort_products():
    sort_by = request.args.get('sort_by', 'name')
    direction = request.args.get('direction', 'asc')
    sorted_products = product_service.sort_products(sort_by, direction)
    return jsonify(sorted_products)

@product_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    limit = request.args.get('limit', default=10, type=int)
    top_products = product_service.get_top_rated_products(limit=limit)
    return jsonify(top_products)

@product_bp.route('/search-history', methods=['POST'])
@jwt_required()
def log_search():
    user_id = get_jwt_identity()
    data = request.get_json()
    search_term = data.get('search_term')
    if not search_term:
        return jsonify({'error': 'Missing search_term'}), 400
    result = product_service.log_search_history(user_id, search_term)
    return jsonify(result)

@product_bp.route('/search-history', methods=['GET'])
@jwt_required()
def get_user_search_history():
    user_id = get_jwt_identity()
    history = product_service.get_search_history(user_id)
    return jsonify(history)


@product_bp.route('/categories', methods=['GET'])
def fetch_unique_categories():
    categories = product_service.get_unique_category_names()
    return jsonify(categories), 200
