from flask import Flask
from config import Config
from extensions import db, migrate, jwt
from flask_cors import CORS 
from app.routes.auth_routes import auth_bp
from app.routes.cart_routes import cart_bp
from app.routes.order_routes import order_bp
from app.routes.user_routes import user_bp
from app.routes.delivery_routes import delivery_bp
from app.routes.product_routes import product_bp
from app.routes.search_history_routes import search_history_bp
from app.services.product_service import ProductService

product_service = ProductService()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(delivery_bp)
    app.register_blueprint(search_history_bp)


    CORS(app)

    return app
