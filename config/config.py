import logging
import os
from functools import lru_cache
from dotenv import load_dotenv
load_dotenv()
FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(filename='userlogging.log',
                    level=logging.INFO, format=FORMAT)


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", None)
    MONGO_URI: str = os.getenv(
        "MONGO_URI", "mongodb://localhost:27017/inventory_db")
    # Email configuration
    DB_NAME = os.getenv("DATABASE_NAME","inventory_db")
    DB_USER = os.getenv("DATABASE_USER","postgres")
    DB_PASSWORD = os.getenv("DATABASE_PASSWORD","postgres")
    DB_HOST = os.getenv("DATABASE_HOST","localhost")
    DB_PORT = os.getenv("DATABASE_PORT", "5432")
    DATABASE_URL = os.getenv("DATABASE_URL", "5432")


settings = Settings()
