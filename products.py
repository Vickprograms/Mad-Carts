from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import DatabaseError
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
    

    def get_product_by_id(self, id):
        """Get a single product by product ID"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, name, category, price, quantity, size, media, description, brand
                    FROM Products WHERE id = %s
                    """, 
                    (id,)
                    )
                product = cur.fetchone()
                if product:
                    return {
                            'id': product[0],
                            'name': product[1],
                            'category': product[2],
                            'price': float(product[3]),
                            'quantity': product[4],
                            'size': product[5],
                            'media': product[6],
                            'description': product[7],
                            'brand': product[8]
                            }, 200
                return {'error': 'Product not found'}, 404
        
        except Exception as e:
            return {'error': str(e)}, 500

    
    def search_autocomplete(self, data):
        """Autocomplete suggestions based on partial match."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, category, price, quantity, size, media, description, brand
                    FROM Products
                    WHERE name ILIKE %s OR category ILIKE %s OR description ILIKE %s OR brand ILIKE %s
                """, (f"%{data}%", f"%{data}%", f"%{data}%", f"%{data}%"))

                rows = cur.fetchall()
                if rows:
                    products = []
                    for row in rows:
                        products.append({
                            'id': row[0],
                            'name': row[1],
                            'category': row[2],
                            'price': float(row[3]),
                            'quantity': row[4],
                            'size': row[5],
                            'media': row[6],
                            'description': row[7],
                            'brand': row[8]
                        })
                    return products, 200
            
                return [{'error': 'No product matches the search'}], 404

        except DatabaseError as e:
            return [{'error': str(e)}], 500

    def get_products_by_category(self,data):

        """get data by Category to enable categorizinn"""

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT  id, name, category, price, quantity, size, media, description, brand
                    FROM Products WHERE category ILIKE %s
                    """, (f"%{data}%",)
                )
                rows = cur.fetchall()
                if rows:
                    products = []
                    for row in rows:
                        products.append({
                            'id': row[0],
                            'name': row[1],
                            'category': row[2],
                            'price': float(row[3]),
                            'quantity': row[4],
                            'size': row[5],
                            'media': row[6],
                            'description': row[7],
                            'brand': row[8]
                        })
                    return products, 200
                
                return jsonify([{
                    'error': 'Category did not match any product category'
                }]), 404
        
        except DatabaseError as e:
            return jsonify({'error': str(e)}), 500

    def create_search_history(self, user_id, search_term):
        """Store search history"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO RecentSearches (id, user_id, search_term, searched_at)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                    """,
                   (
                    str(uuid.uuid4()),
                    user_id,
                    search_term,
                    datetime.utcnow()
                )
                )
                new_search = cur.fetchone()[0]
                self.conn.commit()
                return {'message': 'Search logged', 'search_id': new_search}, 201
        except psycopg2.Error as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

product_manager = Products()



if __name__ == '__main__':
    app.run(debug=True)
