from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, index=True)
    order_type = Column(String)  # BUY or SELL
    price = Column(Float)  # Price per unit
    quantity = Column(Integer)  # Number of units
    status = Column(String, default="PENDING")  # Order status

    # Relationship to link the order to a user
    user = relationship("User")
