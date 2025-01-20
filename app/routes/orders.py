from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User, Order
from app.database import get_db
from app.models import User, Order, Holding


from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User, Order
from app.database import get_db

router = APIRouter()

# Define the request model
class PlaceOrderRequest(BaseModel):
    email: str
    symbol: str
    order_type: str  # BUY or SELL
    price: float
    quantity: int

@router.post("/place_order", tags=["Orders"])
def place_order(
    order_request: PlaceOrderRequest,
    db: Session = Depends(get_db)
):
    """
    Place an order and update the user's holdings.
    """
    email = order_request.email
    symbol = order_request.symbol
    order_type = order_request.order_type
    price = order_request.price
    quantity = order_request.quantity

    # Fetch the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Handle BUY orders
    if order_type.upper() == "BUY":
        total_cost = price * quantity
        if user.balance < total_cost:
            raise HTTPException(status_code=400, detail="Insufficient balance to place the order.")
        user.balance -= total_cost  # Deduct balance

        # Update or create a holding
        holding = db.query(Holding).filter(Holding.user_id == user.id, Holding.symbol == symbol).first()
        if holding:
            # Update existing holding
            new_quantity = holding.quantity + quantity
            new_total_value = holding.total_value + total_cost
            holding.avg_buy_price = new_total_value / new_quantity
            holding.quantity = new_quantity
            holding.total_value = new_total_value
        else:
            # Create new holding
            new_holding = Holding(
                user_id=user.id,
                symbol=symbol,
                quantity=quantity,
                avg_buy_price=price,
                total_value=total_cost
            )
            db.add(new_holding)

    # Handle SELL orders
    elif order_type.upper() == "SELL":
        holding = db.query(Holding).filter(Holding.user_id == user.id, Holding.symbol == symbol).first()
        if not holding or holding.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient quantity in portfolio to sell.")
        holding.quantity -= quantity
        holding.total_value -= quantity * holding.avg_buy_price
        if holding.quantity == 0:
            db.delete(holding)  # Remove holding if quantity reaches zero
        user.balance += price * quantity  # Add funds to balance

    # Commit the transaction
    db.commit()
    db.refresh(user)
    print("Order successfully committed to the database.")
    return {"message": "Order placed successfully", "balance": user.balance}

# Define the request model
class OrderHistoryRequest(BaseModel):
    email: str
    symbol: str = None  # Optional
    order_type: str = None  # Optional

@router.post("/history", tags=["Orders"])
def get_order_history(
    request: OrderHistoryRequest,
    db: Session = Depends(get_db)
):
    """
    Fetch order history for a given user.
    """
    email = request.email
    symbol = request.symbol
    order_type = request.order_type

    # Fetch the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    print(f"Fetching orders for user ID: {user.id}")

    # Query the orders for the user
    query = db.query(Holding).filter(Holding.user_id == user.id)

    # Apply filters
    if symbol:
        query = query.filter(Holding.symbol == symbol)
    if order_type:
        query = query.filter(Holding.order_type == order_type.upper())  # Normalize case

    # Fetch results
    orders = query.all()
    if not orders:
        return {"message": "No orders found for the given criteria."}

    print(f"Fetched {len(orders)} orders.")

    return {
        "orders": [
            {
                "id": order.id,
                "symbol": order.symbol,
                "quantity": order.quantity,
                "avg_buy_price": order.avg_buy_price,
                "total_value": order.total_value
            }
            for order in orders
        ]
    }
