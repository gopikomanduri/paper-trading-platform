# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel  # Import BaseModel from pydantic
# from typing import List

# from sqlalchemy.orm import Session
# from fastapi import APIRouter, Depends, HTTPException
# from app.database import get_db
# from app.models import User, Order  # Adjust based on your model structure

# router = APIRouter()

# # Dummy database for transactions
# transactions_db = []

# # Transaction model
# class Transaction(BaseModel):
#     user_id: int
#     type: str  # e.g., "BUY", "SELL", "CONTEST_ENTRY"
#     amount: float
#     balance: float

# @router.get("/transactions/{user_id}", response_model=List[Transaction], tags=["Transactions"])
# def get_transactions(user_id: int):
#     # Fetch all transactions for the given user ID
#     user_transactions = [tx for tx in transactions_db if tx["user_id"] == user_id]
#     if not user_transactions:
#         raise HTTPException(status_code=404, detail="No transactions found")
#     return user_transactions

# @router.get("/history", tags=["Transactions"])
# def get_transaction_history(
#     email: str,
#     db: Session = Depends(get_db)
# ):
#     """
#     Fetch transaction history for a given user.
#     """
#     # Fetch the user
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Fetch all transactions for the user
#     transactions = db.query(Order).filter(Order.user_id == user.id).all()

#     return {
#         "transactions": [
#             {
#                 "id": txn.id,
#                 "symbol": txn.symbol,
#                 "order_type": txn.order_type,
#                 "price": txn.price,
#                 "quantity": txn.quantity,
#                 "status": txn.status,
#                 "total_value": txn.price * txn.quantity
#             }
#             for txn in transactions
#         ]
#     }


from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User, Order
from app.database import get_db

# Define the request model for transaction history
class TransactionHistoryRequest(BaseModel):
    email: str

router = APIRouter()

@router.post("/history", tags=["Transactions"])
def get_transaction_history(
    request: TransactionHistoryRequest,
    db: Session = Depends(get_db)
):
    """
    Fetch transaction history for a given user.
    """
    # Extract email from the request body
    email = request.email

    # Fetch the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch all transactions for the user
    transactions = db.query(Order).filter(Order.user_id == user.id).all()

    return {
        "transactions": [
            {
                "id": txn.id,
                "symbol": txn.symbol,
                "order_type": txn.order_type,
                "price": txn.price,
                "quantity": txn.quantity,
                "status": txn.status,
                "total_value": txn.price * txn.quantity
            }
            for txn in transactions
        ]
    }
