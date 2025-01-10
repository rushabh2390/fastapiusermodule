from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    date_of_birth = Column(DateTime)
    is_super_user = Column(Boolean, default=False)
    is_staff_user = Column(Boolean, default=False)
