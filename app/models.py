from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, engine
from sqlalchemy.orm import configure_mappers


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float, default=10000.0)

    # Relationship to holdings
    holdings = relationship("Holding", back_populates="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, index=True)
    order_type = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    status = Column(String, default="PENDING")

    # Relationship to link orders with the user
    user = relationship("User", back_populates="orders")


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    avg_buy_price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)

    # Relationship to the user
    user = relationship("User", back_populates="holdings")


# Ensure all mappers are configured
configure_mappers()

# Create tables in the database
Base.metadata.create_all(bind=engine)
print("All tables created successfully!")
