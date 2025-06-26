# models/product.py

import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(50))
    media = db.Column(db.Text)
    description = db.Column(db.Text)
    brand = db.Column(db.String(100))
