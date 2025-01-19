from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt  # Import PyJWT
from app.data_store import users_db, orders_db, transactions_db, inventory_db


# JWT configurations
SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# In-memory user database (for demo purposes; replace with a real database)
users_db = {}

# FastAPI Router
router = APIRouter()

# Models
class User(BaseModel):
    username: str
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper Functions
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@router.post("/register", tags=["Authentication"])
def register(user: User):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    users_db[user.email] = {
        "username": user.username,
        "hashed_password": user.password,  # Add hashing in production
        "balance": 10000.00  # Initialize balance
    }
    return {
        "message": "User registered successfully",
        "balance": users_db[user.email]["balance"]  # Include balance in the response
    }

# @router.post("/login", response_model=Token, tags=["Authentication"])
# def login(email: str, password: str):
#     user = users_db.get(email)
#     if not user or user["hashed_password"] != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": email})
#     return {"access_token": access_token, "token_type": "bearer"}

# Request body model for login
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login", response_model=Token, tags=["Authentication"])
def login(login_request: LoginRequest):
    email = login_request.email
    password = login_request.password

    user = users_db.get(email)
    if not user or user["hashed_password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token", tags=["Authentication"])
def verify_token(token: str):
    decoded_data = decode_access_token(token)
    return {"decoded_data": decoded_data}
