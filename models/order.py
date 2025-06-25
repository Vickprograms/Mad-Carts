import uuid
from datetime import datetime
from sqlalchemy import Column, Float, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db
from marshmallow import Schema, fields, validate, validates_schema, ValidationError




class Order(db.Model):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # e.g., pending, shipped, delivered
    created_at = Column(DateTime, default=datetime.utcnow)

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order id={self.id} user_id={self.user_id} total_amount={self.total_amount}>"


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem id={self.id} product_id={self.product_id} quantity={self.quantity}>"




class OrderItemSchema(Schema):
    id = fields.UUID(dump_only=True)
    product_id = fields.UUID(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    price = fields.Float(required=True)

class OrderSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)
    total_amount = fields.Float(required=True)
    status = fields.String(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    order_items = fields.List(fields.Nested(OrderItemSchema), required=True)

    @validates_schema
    def validate_items_exist(self, data, **kwargs):
        if not data.get("order_items"):
            raise ValidationError("Order must have at least one item.", "order_items")
