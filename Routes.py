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



if __name__ == '__main__':
    app.run(port = 5555, debug = True)