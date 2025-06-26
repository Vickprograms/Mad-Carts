
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request
from app.services.product_service import ProductService

product_routes = Blueprint('product_routes', __name__)
product_service = ProductService()

@product_routes.route('/products', methods=['GET'])
def get_all_products():
    products = product_service.get_all_products()
    return jsonify(products)

@product_routes.route('/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = product_service.get_product_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@product_routes.route('/products/category/<category>', methods=['GET'])
def get_products_by_category(category):
    products = product_service.get_products_by_category(category)
    return jsonify(products)

@product_routes.route('/search-history', methods=['POST'])
@jwt_required()
def log_search():
    user_id = get_jwt_identity()
    data = request.get_json()
    search_term = data.get('search_term')

    if not search_term:
        return jsonify({'error': 'Missing search_term'}), 400

    result = product_service.log_search_history(user_id, search_term)
    return jsonify(result)

@product_routes.route('/recommendations', methods=['GET'])
def get_recommendations():
    limit = request.args.get('limit', default=10, type=int)
    top_products = product_service.get_top_rated_products(limit=limit)
    return jsonify(top_products)
