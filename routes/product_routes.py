from flask import Blueprint, request, jsonify
from controllers.product_controller import product_ctrl

product_bp = Blueprint('product_bp', __name__, url_prefix='/products')

@product_bp.route('/', methods=['GET'])
def get_all():
    result, status = product_ctrl.get_all_products()
    return jsonify(result), status

@product_bp.route('/by-id', methods=['POST'])
def get_product_id():
    data = request.get_json()
    product_id = data.get("id")

    if not product_id:
        return jsonify({"error": "Missing product ID"}), 400

    result, status = product_ctrl.get_product_by_id(product_id)
    return jsonify(result), status

@product_bp.route('/create', methods=['POST'])
def create_product():
    data = request.get_json()
    result, status = product_ctrl.create_product(data)
    return jsonify(result), status
