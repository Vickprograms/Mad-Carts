from flask import Flask,request,jsonify
from  products import Products

product_manager = Products()

app = Flask(__name__)

@app.route('/')
def index():
    return "Products page"


@app.route('/create-product', methods=['POST'])
def create_new_product():
    data = request.get_json()
    result, status = product_manager.create_product(data)
    return jsonify(result), status

@app.route('/Get-all-products', methods = ['GET'])
def get_all():
    result, status = product_manager.get_all_products()
    return jsonify(result), status

@app.route('/get-product-by-id', methods=["POST"])
def get_product_id():
    data = request.get_json()
    
    
    if not data or 'id' not in data:
        return jsonify({'error': 'Missing product ID'}), 400

    product_id = data['id']
    result, status = product_manager.get_product_by_id(product_id)
    return jsonify(result), status

@app.route('/autocomplete', methods=['GET'])
def autocomplete_search():
    data = request.args.get("q", "")
    if not data:
        return jsonify([{
            'error': 'enter search term to search'
        }]), 400

    result, status = product_manager.search_autocomplete(data)
    return jsonify(result), status


@app.route('/category', methods = ['GET'])
def get_by_category():
    data = request.args.get('q', '')
    if not data:
        return jsonify([{
            'error': 'enter a valid category'
        }]), 404
    result, status = product_manager.get_products_by_category(data)
    return jsonify(result), status

@app.route('/create-history', methods=["POST"])
def create_history():
    data = request.get_json()
    if not data or 'search_term' not in data:
        return jsonify({'error': 'No search term provided'}), 400

    user_id = product_manager.get_current_user_id()  
    search_term = data['search_term']

    result, status = product_manager.create_search_history(user_id, search_term)
    return jsonify({'search_term': search_term}), status

@app.route('/history', methods=['GET'])
def get_history():
    user_id = product_manager.get_current_user_id()
    
    if not user_id:
        return jsonify({'error': 'User not authenticated'}), 401

    result, status = product_manager.get_search_history(user_id)
    return jsonify(result), status

@app.route('/Clear-history', methods = ['DELETE'])
def Clear_history():
    data = request.get_json()
    if not data and id in data:
        return jsonify([{
            'error': 'No search is found to delete'
        }]), 404

    id = data['id']
    result, status = product_manager.delete_history(id)
    return jsonify(result), status    


@app.route('/delete-product', methods=["DELETE"])
def remove_product():
    data = request.get_json()

    if not data or 'id' not in data:
        return jsonify([{
            'error': 'Enter product_id to delete'
        }]), 400

    product_id = data['id']
    result, status = product_manager.delete_product(product_id)
    return jsonify(result), status

@app.route('/update-product/<product_id>', methods=["PATCH"])
def update_product(product_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    result, status = product_manager.update_product(product_id, data)
    return jsonify(result), status


@app.route('/replace-product/<product_id>', methods=["PUT"])
def replace_product(product_id):
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    result, status = product_manager.replace_product(product_id, data)
    return jsonify(result), status


if __name__ == '__main__':
    app.run(port = 5555, debug = True)