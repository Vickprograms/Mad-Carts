import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path


env_path = "/home/gideon/Mad-cartsBackend/Mad-Carts/.env"
load_dotenv(dotenv_path=env_path, override=True)

def get_db_connection():
    

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS")
    )
