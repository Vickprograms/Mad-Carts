from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2 import DatabaseError
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

product_bp = Blueprint('products', __name__)

class ProductController:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            sslmode="require"
        )

    def _dict_from_row(self, row):
        return {
            'id': row[0],
            'name': row[1],
            'category': row[2],
            'price': float(row[3]),
            'quantity': row[4],
            'size': row[5],
            'media': row[6],
            'description': row[7],
            'brand': row[8]
        }

    def create_product(self, data):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO products (id, name, category, price, quantity, size, media, description, brand)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """, (
                    str(uuid.uuid4()),
                    data.get('name'),
                    data.get('category'),
                    data.get('price'),
                    data.get('quantity'),
                    data.get('size'),
                    data.get('media'),
                    data.get('description'),
                    data.get('brand')
                ))
                new_id = cur.fetchone()[0]
                self.conn.commit()
                return {'message': 'Product created', 'id': new_id}, 201
        except psycopg2.Error as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

    def get_all_products(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM products")
                rows = cur.fetchall()
                products = [self._dict_from_row(row) for row in rows]
                return products, 200 if products else ({'error': 'No products found'}, 404)
        except DatabaseError as e:
            return {'error': str(e)}, 500

    def get_product_by_id(self, product_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                row = cur.fetchone()
                return self._dict_from_row(row), 200 if row else ({'error': 'Product not found'}, 404)
        except Exception as e:
            return {'error': str(e)}, 500

product_ctrl = ProductController()

@product_bp.route('/', methods=['GET'])
def get_all():
    return product_ctrl.get_all_products()

@product_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return product_ctrl.create_product(data)

@product_bp.route('/all', methods=['GET'])
def get_all():
    return product_ctrl.get_all_products()

@product_bp.route('/<product_id>', methods=['GET'])
def get_by_id(product_id):
    return product_ctrl.get_product_by_id(product_id)
