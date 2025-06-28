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
        image = request.files.get('image')

        # Required fields
        required = ['name', 'price', 'category', 'description', 'quantity', 'size', 'brand']
        missing = [field for field in required if not data.get(field)]
        if missing:
            return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 422

        # 🧹 Sanitize + Cast
        try:
            data['price'] = float(data['price'])
            data['quantity'] = int(data['quantity'])
        except ValueError:
            return jsonify({'error': 'Price must be a number and quantity must be an integer'}), 422

        # Image upload
        media_path = None
        if image:
            filename = secure_filename(image.filename)
            upload_dir = os.path.join(current_app.root_path, 'static/uploads')
            os.makedirs(upload_dir, exist_ok=True)
            upload_path = os.path.join(upload_dir, filename)
            image.save(upload_path)
            media_path = f'static/uploads/{filename}'

        # Log for debug
        print("📦 Final sanitized form data:", data)
        print("🖼️ Media path:", media_path)

        # Call the service
        product_id = product_service.create_product(data, media_path)

        return jsonify({'message': 'Product created', 'product_id': product_id}), 201

    except Exception as e:
        print("❌ Error during product creation:", str(e))
        return jsonify({'error': str(e)}), 500


def update_product_controller(product_id):
    try:
        data = request.form.to_dict()
        image = request.files.get('image')

        if image:
            
            filename = secure_filename(image.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            image.save(upload_path)
            data['media'] = filename 

        product_service.update_product(product_id, data)
        return jsonify({'message': 'Product updated'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def partial_update_product_controller(product_id):
    try:
        data = request.form.to_dict()
        image = request.files.get('image')

        
        if image:
            filename = secure_filename(image.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            image.save(upload_path)
            data['media'] = filename  

        
        product_service.partial_update_product(product_id, data)
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
    term = request.args.get('term', '').strip()
    try:
        products = product_service.search_products(term)
        return jsonify(products), 200
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

def get_unique_categories():
    result = db.session.execute(db.select(Product.category).distinct())
    return [row[0] for row in result if row[0] is not None]