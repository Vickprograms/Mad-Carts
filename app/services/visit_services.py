from app.utils.db import get_db_connection
from psycopg2.extras import RealDictCursor

class VisitService:
    def __init__(self):
        self.conn = get_db_connection()

    def log_visit(self, user_id, product_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO RecentVisits (user_id, product_id)
                VALUES (%s, %s)
                RETURNING *;
            """, (user_id, product_id))
            self.conn.commit()
            return cur.fetchone(), 201

    def get_recent_visits(self, user_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT rv.*, p.name, p.media, p.price
                FROM RecentVisits rv
                JOIN Products p ON rv.product_id = p.id
                WHERE rv.user_id = %s
                ORDER BY rv.visited_at DESC
                LIMIT 20;
            """, (user_id,))
            return cur.fetchall(), 200
