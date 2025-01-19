from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # Import BaseModel from pydantic
from typing import List

router = APIRouter()

# Dummy database for transactions
transactions_db = []

# Transaction model
class Transaction(BaseModel):
    user_id: int
    type: str  # e.g., "BUY", "SELL", "CONTEST_ENTRY"
    amount: float
    balance: float

@router.get("/transactions/{user_id}", response_model=List[Transaction], tags=["Transactions"])
def get_transactions(user_id: int):
    # Fetch all transactions for the given user ID
    user_transactions = [tx for tx in transactions_db if tx["user_id"] == user_id]
    if not user_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return user_transactions
