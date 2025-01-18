from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# In-memory databases
orders_db = []
inventory_db = {}

class Order(BaseModel):
    user_id: int
    symbol: str
    order_type: str  # "BUY" or "SELL"
    price: float
    quantity: int

@router.post("/place_order", tags=["Orders"])
def place_order(order: Order):
    user_inventory = inventory_db.get(order.user_id, {})
    if order.order_type == "SELL":
        if order.symbol not in user_inventory or user_inventory[order.symbol] < order.quantity:
            raise HTTPException(status_code=400, detail="Insufficient inventory")
        user_inventory[order.symbol] -= order.quantity
    elif order.order_type == "BUY":
        user_inventory[order.symbol] = user_inventory.get(order.symbol, 0) + order.quantity
    else:
        raise HTTPException(status_code=400, detail="Invalid order type")
    orders_db.append(order.dict())
    return {"message": "Order placed successfully", "order": order}

@router.get("/get_orders", response_model=List[Order], tags=["Orders"])
def get_orders():
    return orders_db
