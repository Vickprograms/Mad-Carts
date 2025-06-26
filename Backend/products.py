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

    def get_unique_categories(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT category FROM Products
                """)
                rows = cur.fetchall()
                categories = [row[0] for row in rows if row[0] is not None]
                return categories, 200
        except Exception as e:
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
    
    def get_search_history(self, user_id):
        """Get search history for a user."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, search_term, searched_at 
                    FROM RecentSearches
                    WHERE user_id = %s
                    ORDER BY searched_at DESC
                    """,
                    (user_id,)
                )
                rows = cur.fetchall()
                if not rows:
                    return {'error': 'No search history found'}, 404

                history = []
                for row in rows:
                    history.append({
                        'id': row[0],
                        'search_term': row[1],
                        'searched_at': row[2]
                    })

                return history, 200

        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return {'error': str(e)}, 500
    
    def delete_history(self, id):
        """Delete history"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM RecentSearches 
                    WHERE id = %s 
                    RETURNING id, user_id, search_term, searched_at
                    """,
                    (id,)
                )
                row = cur.fetchone()

                if not row:
                    return {'error': 'No recent search with that id to delete'}, 404

                search = {
                    'id': row[0],
                    'user_id': row[1],
                    'search_term': row[2],
                    'searched_at': row[3]
                }

                self.conn.commit()
                return search, 200

        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

    def delete_product(self, product_id):
        """Delete a product by ID."""
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM Products WHERE id = %s RETURNING id, name, category, price, quantity, size, media, description, brand",
                    (product_id,)
                )
                row = cur.fetchone()
                if not row:
                    return {'error': 'No product with that ID to delete'}, 404

                product = {
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
                self.conn.commit()
                return product, 200

        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            return {'error': str(e)}, 500
    

    def update_product(self, product_id, data):
        try:
            with self.conn.cursor() as cur:
                fields = []
                values = []
                for key, value in data.items():
                    fields.append(f"{key} = %s")
                    values.append(value)

                values.append(product_id)
                query = f"UPDATE Products SET {', '.join(fields)} WHERE id = %s RETURNING *;"
                cur.execute(query, values)
                updated = cur.fetchone()
                self.conn.commit()

                if updated:
                    return {'message': 'Product updated', 'product_id': product_id}, 200
                else:
                    return {'error': 'Product not found'}, 404
        except Exception as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

    def replace_product(self, product_id, data):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    UPDATE Products
                    SET name = %s, category = %s, price = %s, quantity = %s,
                    size = %s, media = %s, description = %s, brand = %s
                    WHERE id = %s RETURNING *;
                """, (
                    data['name'], data['category'], data['price'],
                    data['quantity'], data['size'], data['media'],
                    data['description'], data['brand'], product_id
                ))
                updated = cur.fetchone()
                self.conn.commit()

                if updated:
                    return {'message': 'Product fully replaced', 'product_id': product_id}, 200
                else:
                    return {'error': 'Product not found'}, 404
        
        except Exception as e:
            self.conn.rollback()
            return {'error': str(e)}, 500

product_manager = Products()



if __name__ == '__main__':
    app.run(debug=True)
