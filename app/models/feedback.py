import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_message = db.Column(db.Text)
    media = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
