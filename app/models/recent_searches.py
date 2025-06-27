import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class RecentSearches(db.Model):
    __tablename__ = 'recent_searches'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    search_term = db.Column(db.Text, nullable=False)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
