# models/recent_visits.py

import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class RecentVisits(db.Model):
    __tablename__ = 'recent_visits'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'))
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id', ondelete='CASCADE'))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
