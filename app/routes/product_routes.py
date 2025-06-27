from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from app.models.product import Product
from app.services.product_service import ProductService

product_bp = Blueprint('product_routes', __name__, url_prefix='/api/products')
product_service = ProductService()

@product_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.form.to_dict()
    image = request.files.get('image')
    result = product_service.create_product(data, image)
    return jsonify(result), 201

@product_bp.route('/products', methods=['GET'])
def get_all_products():
    products = product_service.get_all_products()
    return jsonify(products)

@product_bp.route('/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@product_bp.route('/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.form.to_dict()
    image = request.files.get('image')
    product_service.update_product(product_id, data, image)
    return jsonify({'message': 'Product updated'})

@product_bp.route('/<product_id>', methods=['PATCH'])
@jwt_required()
def partial_update_product(product_id):
    data = request.form.to_dict()
    image = request.files.get('image')
    product_service.partial_update_product(product_id, data, image)
    return jsonify({'message': 'Product partially updated'})

@product_bp.route('/<product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product_service.delete_product(product_id)
    return jsonify({'message': 'Product deleted'})

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
