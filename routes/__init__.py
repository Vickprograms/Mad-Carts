from flask import Flask
from extensions import db, migrate
from config import Config


from routes.cart_routes import cart_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    db.init_app(app)
    migrate.init_app(app, db)

    
    app.register_blueprint(cart_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return {"message": "Mad-Carts is up and running "}

    return app
