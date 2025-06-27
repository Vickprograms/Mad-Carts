import uuid
from datetime import datetime
import psycopg2

class SearchHistoryService:
    def __init__(self, conn):
        self.conn = conn

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
        """Delete a specific search history entry."""
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