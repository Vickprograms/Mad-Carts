from flask import Flask
from config import Config
from extensions import db, migrate, jwt
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app