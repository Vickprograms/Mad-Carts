from flask import Flask, request, jsonify
import psycopg2
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

class Products:

    def __init__(self):
        """Initialize database connection"""
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            sslmode="require"
        )
        print("DB_HOST:", os.getenv("DB_HOST"))
        print("DB_NAME:", os.getenv("DB_NAME"))
        print("DB_USER:", os.getenv("DB_USER"))
        print("DB_PASS:", os.getenv("DB_PASS"))


    def create_product(self, data):
        """Insert product into DB and return result"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO products (id, name, category, price, quantity, size, media, description, brand)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        str(uuid.uuid4()),
                        data.get('name'),
                        data.get('category'),
                        data.get('price'),
                        data.get('quantity'),
                        data.get('size'),
                        data.get('media'),
                        data.get('description'),
                        data.get('brand')
                    )
                )
                new_id = cur.fetchone()[0]
                self.conn.commit()
                return {'message': 'Product created', 'id': new_id}, 201
        except psycopg2.Error as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

    def get_all_products(self):
        """Get all products from the database"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, category, price, quantity, size, media, description, brand
                    FROM Products
                    """
                )
                rows = cur.fetchall()
                if rows:
                    products = []
                    for row in rows:
                        products.append({
                            'id': row[0],
                            'name': row[1],
                            'category': row[2],
                            'price': row[3],
                            'quantity': row[4],
                            'size': row[5],
                            'media': row[6],
                            'description': row[7],
                            'brand': row[8]
                        })
                    return products, 200

                return jsonify({'error': 'No products found!'}), 404

        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500



product_manager = Products()


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

if __name__ == '__main__':
    app.run(port=5555, debug=True)
