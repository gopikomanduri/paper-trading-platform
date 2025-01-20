from app.database import SessionLocal
from app.models import User, Holding

db = SessionLocal()
user = db.query(User).filter(User.email == "test@example.com").first()
print(user.holdings)

# Create a test user and holding
test_user = User(email="b@b.com", username="b", hashed_password="b")
db.add(test_user)
db.commit()

holding = Holding(user_id=test_user.id, symbol="AAPL", quantity=10, avg_buy_price=150.0, total_value=1500.0)
db.add(holding)
db.commit()

# Query the user and check their holdings
user = db.query(User).filter(User.email == "b@b.com").first()
print(user.holdings)
