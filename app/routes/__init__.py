from flask import Flask
from extensions import db, migrate
from config import Config
from app.routes.cart_routes import cart_bp
from app.routes.auth_routes import auth_bp
from app.routes.order_routes import order_bp
from app.routes.user_routes import user_bp
from app.routes.delivery_routes import delivery_bp
from app.routes.product_routes import product_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(user_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(product_bp, url_prefix="/products")

    @app.route('/')
    def home():
        return {"message": "Mad-Carts is up and running"}

    return app
