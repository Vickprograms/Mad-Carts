from flask import request, jsonify
from app.services.product_service import ProductService

product_service = ProductService()

def get_all_products_controller():
    try:
        products = product_service.get_all_products()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_product_by_id_controller(product_id):
    try:
        product = product_service.get_product_by_id(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        return jsonify(product), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_product_controller():
    try:
        data = request.form.to_dict()
        image = request.files.get('image')  # 'image' is the field name in the form

        product_id = product_service.create_product(data, image)
        return jsonify({'message': 'Product created', 'product_id': product_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def update_product_controller(product_id):
    try:
        data = request.form.to_dict()
        image = request.files.get('image')

        product_service.update_product(product_id, data, image)
        return jsonify({'message': 'Product updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def partial_update_product_controller(product_id):
    try:
        data = request.form.to_dict()
        image = request.files.get('image')

        product_service.partial_update_product(product_id, data, image)
        return jsonify({'message': 'Product partially updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def delete_product_controller(product_id):
    try:
        product_service.delete_product(product_id)
        return jsonify({'message': 'Product deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def search_products_controller():
    try:
        term = request.args.get('term', '')
        results = product_service.search_products(term)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def filter_products_controller():
    try:
        filters = request.args.to_dict()
        filtered = product_service.filter_products(filters)
        return jsonify(filtered), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def sort_products_controller():
    try:
        sort_by = request.args.get('sort_by', 'name')
        direction = request.args.get('direction', 'asc')
        sorted_products = product_service.sort_products(sort_by, direction)
        return jsonify(sorted_products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
