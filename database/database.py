import os
from config.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists, create_database

settings = settings
# SQLALCHEMY_DATABASE_URL = settings.Data
# print(SQLALCHEMY_DATABASE_URL,  os.getenv("DATABASE_URL"))

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))