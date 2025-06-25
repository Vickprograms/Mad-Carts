from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from models.cart import Cart
from models.order import Order
from extensions import db
from marshmallow import EXCLUDE


class CartSchema(SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    user_id = auto_field(required=True)
    
    class Meta:
        model = Cart
        load_instance = True
        sqla_session = db.session
        include_fk = True
        unknown = EXCLUDE


class OrderSchema(SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    user_id = auto_field(required=True)

    class Meta:
        model = Order
        load_instance = True
        sqla_session = db.session
        include_fk = True
        unknown = EXCLUDE
