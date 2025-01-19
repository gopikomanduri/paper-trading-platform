from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.data_store import users_db, orders_db, transactions_db, inventory_db  # Shared data store

router = APIRouter()

# Models
class Order(BaseModel):
    email: str  # Identify user by email
    symbol: str
    order_type: str  # "BUY" or "SELL"
    price: float
    quantity: int

class OrderResponse(BaseModel):
    id: int
    email: str
    symbol: str
    order_type: str
    price: float
    quantity: int
    status: str

# # Place an order
# @router.post("/place_order", response_model=OrderResponse, tags=["Orders"])
# def place_order(order: Order):
#     # Look up the user by email
#     user = users_db.get(order.email)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     cost = order.price * order.quantity

#     # Handle BUY order
#     if order.order_type == "BUY":
#         if user["balance"] < cost:
#             raise HTTPException(status_code=400, detail="Insufficient balance")
#         user["balance"] -= cost
#         inventory_db[order.email] = inventory_db.get(order.email, {})
#         inventory_db[order.email][order.symbol] = inventory_db[order.email].get(order.symbol, 0) + order.quantity

#     # Handle SELL order
#     elif order.order_type == "SELL":
#         inventory = inventory_db.get(order.email, {})
#         if inventory.get(order.symbol, 0) < order.quantity:
#             raise HTTPException(status_code=400, detail="Insufficient inventory")
#         inventory[order.symbol] -= order.quantity
#         user["balance"] += cost

#     else:
#         raise HTTPException(status_code=400, detail="Invalid order type")

#     # Save the order
#     order_id = len(orders_db) + 1
#     orders_db.append({
#         "id": order_id,
#         "email": order.email,
#         "symbol": order.symbol,
#         "order_type": order.order_type,
#         "price": order.price,
#         "quantity": order.quantity,
#         "status": "COMPLETED"
#     })

#     # Log the transaction
#     transactions_db.append({
#         "email": order.email,
#         "type": order.order_type,
#         "amount": -cost if order.order_type == "BUY" else cost,
#         "balance": user["balance"]
#     })

#     return {
#         "id": order_id,
#         "email": order.email,
#         "symbol": order.symbol,
#         "order_type": order.order_type,
#         "price": order.price,
#         "quantity": order.quantity,
#         "status": "COMPLETED"
#     }


@router.post("/place_order", response_model=OrderResponse, tags=["Orders"])
def place_order(order: Order):
    # Debugging: Print the current users_db and the email being searched
    print("Current users_db:", users_db)
    print("Order email:", order.email)

    # Normalize email to lowercase for consistent lookups
    user = users_db.get(order.email.lower())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cost = order.price * order.quantity

    # Handle BUY order
    if order.order_type == "BUY":
        if user["balance"] < cost:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user["balance"] -= cost
        inventory_db[order.email] = inventory_db.get(order.email, {})
        inventory_db[order.email][order.symbol] = inventory_db[order.email].get(order.symbol, 0) + order.quantity

    # Handle SELL order
    elif order.order_type == "SELL":
        inventory = inventory_db.get(order.email, {})
        if inventory.get(order.symbol, 0) < order.quantity:
            raise HTTPException(status_code=400, detail="Insufficient inventory")
        inventory[order.symbol] -= order.quantity
        user["balance"] += cost

    else:
        raise HTTPException(status_code=400, detail="Invalid order type")

    # Save the order
    order_id = len(orders_db) + 1
    orders_db.append({
        "id": order_id,
        "email": order.email,
        "symbol": order.symbol,
        "order_type": order.order_type,
        "price": order.price,
        "quantity": order.quantity,
        "status": "COMPLETED"
    })

    # Log the transaction
    transactions_db.append({
        "email": order.email,
        "type": order.order_type,
        "amount": -cost if order.order_type == "BUY" else cost,
        "balance": user["balance"]
    })

    return {
        "id": order_id,
        "email": order.email,
        "symbol": order.symbol,
        "order_type": order.order_type,
        "price": order.price,
        "quantity": order.quantity,
        "status": "COMPLETED"
    }

# Get all orders
@router.get("/get_orders", response_model=List[OrderResponse], tags=["Orders"])
def get_orders():
    return orders_db
