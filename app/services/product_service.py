from app.utils.db import get_db_connection
import uuid
from datetime import datetime

class ProductService:
    def __init__(self):
        self.conn = get_db_connection()

    def get_all_products(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM products")
            return cur.fetchall()

    def get_product_by_id(self, product_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            return cur.fetchone()

    def create_product(self, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (id, name, category, price, quantity, size, media, description, brand)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                str(uuid.uuid4()), data['name'], data['category'],
                data['price'], data['quantity'], data['size'],
                data['media'], data['description'], data['brand']
            ))
            product_id = cur.fetchone()[0]
            self.conn.commit()
            return product_id

    def update_product(self, product_id, data):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE products
                SET name=%s, category=%s, price=%s, quantity=%s, size=%s, media=%s, description=%s, brand=%s
                WHERE id=%s
            """, (
                data['name'], data['category'], data['price'], data['quantity'],
                data['size'], data['media'], data['description'], data['brand'], product_id
            ))
            self.conn.commit()

    def partial_update_product(self, product_id, updates):
        fields = ', '.join(f"{key}=%s" for key in updates)
        values = list(updates.values())
        values.append(product_id)
        query = f"UPDATE products SET {fields} WHERE id=%s"
        with self.conn.cursor() as cur:
            cur.execute(query, values)
            self.conn.commit()
    
     

    def delete_product(self, product_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id=%s", (product_id,))
            self.conn.commit()

    def search_products(self, term):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM products
                WHERE name ILIKE %s OR description ILIKE %s
            """, (f"%{term}%", f"%{term}%"))
            return cur.fetchall()

    def filter_products(self, filters):
        query = "SELECT * FROM products WHERE "
        clauses = []
        values = []

        for key, value in filters.items():
            clauses.append(f"{key} = %s")
            values.append(value)

        query += " AND ".join(clauses)

        with self.conn.cursor() as cur:
            cur.execute(query, tuple(values))
            return cur.fetchall()

    def sort_products(self, sort_by, direction):
        query = f"SELECT * FROM products ORDER BY {sort_by} {direction.upper()}"
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


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


    def get_top_rated_products(self, limit=10):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        p.id, p.name, p.description, p.price, p.image_url, 
                        AVG(f.rating) AS avg_rating, COUNT(f.id) AS num_reviews
                    FROM Products p
                    JOIN Feedback f ON p.id = f.product_id
                    GROUP BY p.id
                    HAVING COUNT(f.id) > 0
                    ORDER BY avg_rating DESC, num_reviews DESC
                    LIMIT %s
                """, (limit,))
                rows = cur.fetchall()

                recommendations = []
                for row in rows:
                    recommendations.append({
                        'id': row[0],
                        'name': row[1],
                        'description': row[2],
                        'price': row[3],
                        'image_url': row[4],
                        'average_rating': float(row[5]),
                        'total_reviews': row[6]
                    })

                return recommendations

        except Exception as e:
            self.conn.rollback()
            return {'error': str(e)}
        