from flask import Flask
from flask_cors import CORS
from extensions import db, migrate, jwt

from app.routes.auth_routes import auth_bp
from app.routes.cart_routes import cart_bp
from app.routes.order_routes import order_bp
from app.routes.delivery_routes import delivery_bp
from app.routes.user_routes import user_bp
from app.routes.product_routes import product_bp
from app.routes.search_history_routes import search_history_bp
from app.routes.visit_routes import visit_bp

def create_app():
    app = Flask(__name__)

    from config import Config
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}}, supports_credentials=True)


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(delivery_bp, url_prefix="/api/deliveries")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(search_history_bp, url_prefix="/api/search")
    app.register_blueprint(visit_bp, url_prefix="/api/visit")
    return app
