import uuid
from datetime import datetime
from sqlalchemy import Column, Float, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

 
class Cart(db.Model):
    __tablename__ = 'carts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart id={self.id} user_id={self.user_id}>"

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey('carts.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    cart = relationship("Cart", back_populates="cart_items")

    def __repr__(self):
        return f"<CartItem id={self.id} product_id={self.product_id} quantity={self.quantity}>"

class CartItemSchema(Schema):
    id = fields.UUID(dump_only=True)
    product_id = fields.UUID(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Float(required=True)

    @validates_schema
    def validate_price_quantity(self, data, **kwargs):
        if data['price'] <= 0:
            raise ValidationError("Price must be greater than zero.")
        if data['quantity'] < 1:
            raise ValidationError("Quantity must be at least 1.")

class CartSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    created_at = fields.DateTime(dump_only=True)
    cart_items = fields.List(fields.Nested(CartItemSchema))