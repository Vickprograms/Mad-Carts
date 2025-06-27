import uuid
from extensions import db
from sqlalchemy.dialects.postgresql import UUID

class Delivery(db.Model):
    __tablename__ = 'deliveries'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    driver_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete="SET NULL"))
    status = db.Column(db.String(50), default='Pending')
    delivery_date = db.Column(db.Date)
    delivery_notes = db.Column(db.Text)
    delivered_at = db.Column(db.DateTime)

    def serialize(self):
        return {
            "id": str(self.id),
            "order_id": str(self.order_id),
            "driver_id": str(self.driver_id) if self.driver_id else None,
            "status": self.status,
            "delivery_date": str(self.delivery_date) if self.delivery_date else None,
            "delivery_notes": self.delivery_notes,
            "delivered_at": str(self.delivered_at) if self.delivered_at else None
        }
