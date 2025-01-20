# app/models/user.py

from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from sqlalchemy.orm import relationship
from app.database import Base, engine
from sqlalchemy.orm import configure_mappers

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Float, default=10000.0)

    # Define the relationship to holdings
    holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")

