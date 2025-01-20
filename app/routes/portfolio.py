from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User, Holding
from app.database import get_db


router = APIRouter()

# @router.get("/portfolio", tags=["Portfolio"])
# def get_portfolio(email: str, db: Session = Depends(get_db)):
#     """
#     Fetch the user's portfolio.
#     """
#     # Fetch the user
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Fetch holdings for the user
#     holdings = db.query(Holding).filter(Holding.user_id == user.id).all()

#     # Return holdings
#     return {
#         "portfolio": [
#             {
#                 "symbol": holding.symbol,
#                 "quantity": holding.quantity,
#                 "avg_buy_price": holding.avg_buy_price,
#                 "total_value": holding.total_value
#             }
#             for holding in holdings
#         ]
#     }

@router.get("/portfolio", tags=["Portfolio"])
 
def get_portfolio(email: str, db: Session = Depends(get_db)):
    """
    Fetch the user's portfolio.
    """
    # Fetch the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch holdings for the user
    holdings = db.query(Holding).filter(Holding.user_id == user.id).all()

    # Return holdings
    return {
        "portfolio": [
            {
                "symbol": holding.symbol,
                "quantity": holding.quantity,
                "avg_buy_price": holding.avg_buy_price,
                "total_value": holding.total_value
            }
            for holding in holdings
        ]
    }

