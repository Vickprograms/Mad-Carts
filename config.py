import os
from dotenv import load_dotenv
from pathlib import Path


env_path = "/home/gideon/Mad-cartsBackend/Mad-Carts/.env"
print(f">>> Loading environment from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    print("Loaded DATABASE_URL:", SQLALCHEMY_DATABASE_URI)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-dev-key")
