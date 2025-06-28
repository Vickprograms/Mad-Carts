import uuid
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Boolean, String

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_no = db.Column(db.String(20))
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    is_driver = db.Column(db.Boolean, default=False)
    role = db.Column(db.String, nullable=False, default='customer')


    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def serialize(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "phone_no": self.phone_no,
            "role": self.role
        }
