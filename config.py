import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://mad_carts_user:ExU8Lz8VDgxBVVbQXCHP0AefguK4Vlzt@localhost:5432/mad_carts"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-dev-key")
    