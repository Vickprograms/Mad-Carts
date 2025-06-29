import os
from dotenv import load_dotenv
from pathlib import Path

# Dynamically load .env from the root of the project
env_path = Path(__file__).resolve().parent / ".env"
print(f">>> Loading environment from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-dev-key")
