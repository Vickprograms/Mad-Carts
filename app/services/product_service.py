import uuid
from datetime import datetime
from psycopg2 import DatabaseError
from werkzeug.utils import secure_filename
import os

from app.utils.db import get_db_connection


class ProductService:
    def __init__(self):
        self.conn = get_db_connection()

    def _serialize(self, row):
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

    def _save_image(self, image):
        if image:
            filename = f"{uuid.uuid4()}_{secure_filename(image.filename)}"
            filepath = os.path.join("uploads", filename)
            image.save(filepath)
            return filepath
        return None

    def create_product(self, data, image=None):
        media_path = self._save_image(image)

        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO products (id, name, category, price, quantity, size, media, description, brand)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                str(uuid.uuid4()), data['name'], data['category'],
                data['price'], data['quantity'], data['size'],
                media_path, data['description'], data['brand']
            ))
            product_id = cur.fetchone()[0]
            self.conn.commit()
            return {'message': 'Product created', 'id': product_id}

    def get_all_products(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            return [self._serialize(row) for row in rows]

    def get_product_by_id(self, product_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
            return self._serialize(row) if row else None

    def update_product(self, product_id, data, image=None):
        media_path = self._save_image(image) if image else data.get("media")

        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE products SET
                    name=%s, category=%s, price=%s, quantity=%s, size=%s,
                    media=%s, description=%s, brand=%s
                WHERE id=%s
            """, (
                data['name'], data['category'], data['price'], data['quantity'],
                data['size'], media_path, data['description'], data['brand'],
                product_id
            ))
            self.conn.commit()
            return {'message': 'Product updated'}

    def partial_update_product(self, product_id, updates, image=None):
        if image:
            updates['media'] = self._save_image(image)

        fields = ', '.join(f"{key} = %s" for key in updates.keys())
        values = list(updates.values()) + [product_id]
        query = f"UPDATE products SET {fields} WHERE id = %s"

        with self.conn.cursor() as cur:
            cur.execute(query, values)
            self.conn.commit()
            return {'message': 'Product partially updated'}

    def delete_product(self, product_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            self.conn.commit()
            return {'message': 'Product deleted'}

    def search_products(self, term):
        with self.conn.cursor() as cur:
            query = """
                SELECT * FROM products
                WHERE name ILIKE %s OR description ILIKE %s OR category ILIKE %s OR brand ILIKE %s
            """
            term_wild = f"%{term}%"
            cur.execute(query, (term_wild, term_wild, term_wild, term_wild))
            rows = cur.fetchall()
            return [self._serialize(row) for row in rows]

    def filter_products(self, filters):
        if not filters:
            return []

        clauses = [f"{key} = %s" for key in filters]
        values = list(filters.values())
        query = f"SELECT * FROM products WHERE {' AND '.join(clauses)}"

        with self.conn.cursor() as cur:
            cur.execute(query, values)
            rows = cur.fetchall()
            return [self._serialize(row) for row in rows]

    def sort_products(self, sort_by='name', direction='asc'):
        if sort_by not in ['name', 'price', 'category', 'brand']:
            sort_by = 'name'
        if direction.lower() not in ['asc', 'desc']:
            direction = 'asc'

        query = f"SELECT * FROM products ORDER BY {sort_by} {direction.upper()}"
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [self._serialize(row) for row in rows]

    def get_products_by_category(self, category):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM products WHERE category ILIKE %s
            """, (f"%{category}%",))
            rows = cur.fetchall()
            return [self._serialize(row) for row in rows]

    def get_top_rated_products(self, limit=10):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    p.id, p.name, p.description, p.price, p.media,
                    AVG(f.rating) AS avg_rating, COUNT(f.id) AS num_reviews
                FROM products p
                JOIN feedback f ON p.id = f.product_id
                GROUP BY p.id
                HAVING COUNT(f.id) > 0
                ORDER BY avg_rating DESC, num_reviews DESC
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()

            return [{
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': float(row[3]),
                'media': row[4],
                'average_rating': float(row[5]),
                'total_reviews': row[6]
            } for row in rows]

    def log_search_history(self, user_id, search_term):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO RecentSearches (id, user_id, search_term, searched_at)
                    VALUES (%s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()), user_id, search_term, datetime.utcnow()
                ))
                self.conn.commit()
                return {'message': 'Search logged'}
        except Exception as e:
            self.conn.rollback()
            return {'error': str(e)}

    def get_search_history(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT search_term, searched_at
                FROM RecentSearches
                WHERE user_id = %s
                ORDER BY searched_at DESC
            """, (user_id,))
            rows = cur.fetchall()
            return [{'term': row[0], 'time': row[1].isoformat()} for row in rows]
    
    def get_unique_categories(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL")
            rows = cur.fetchall()
            return [row[0] for row in rows if row[0]]  