# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# import jwt  # Import PyJWT
# from app.data_store import users_db, orders_db, transactions_db, inventory_db

# from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models import User
# from app.database import get_db


# # JWT configurations
# SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # In-memory user database (for demo purposes; replace with a real database)
# users_db = {}

# # FastAPI Router
# router = APIRouter()

# # Models
# class User(BaseModel):
#     username: str
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Helper Functions
# def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def decode_access_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")

# # Routes
# @router.post("/register", tags=["Authentication"])
# def register(user: User):
#     if user.email in users_db:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     users_db[user.email] = {
#         "username": user.username,
#         "hashed_password": user.password,  # Add hashing in production
#         "balance": 10000.00  # Initialize balance
#     }
#     return {
#         "message": "User registered successfully",
#         "balance": users_db[user.email]["balance"]  # Include balance in the response
#     }

# # @router.post("/login", response_model=Token, tags=["Authentication"])
# # def login(email: str, password: str):
# #     user = users_db.get(email)
# #     if not user or user["hashed_password"] != password:
# #         raise HTTPException(status_code=401, detail="Invalid credentials")
# #     access_token = create_access_token(data={"sub": email})
# #     return {"access_token": access_token, "token_type": "bearer"}

# # Request body model for login
# class LoginRequest(BaseModel):
#     email: str
#     password: str

# @router.post("/login", response_model=Token, tags=["Authentication"])
# def login(login_request: LoginRequest):
#     email = login_request.email
#     password = login_request.password

#     user = users_db.get(email)
#     if not user or user["hashed_password"] != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     access_token = create_access_token(data={"sub": email})
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.get("/verify-token", tags=["Authentication"])
# def verify_token(token: str):
#     decoded_data = decode_access_token(token)
#     return {"decoded_data": decoded_data}


# @router.post("/auth/register")
# def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
#     # Check if the user already exists
#     db_user = db.query(User).filter(User.email == email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     # Add new user
#     new_user = User(username=username, email=email, hashed_password=password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully", "user": new_user}



from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt  # Using PyJWT
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User as DBUser
from app.models.user import User  # Import User directly


# JWT Configurations
SECRET_KEY = "your_secret_key"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI Router
router = APIRouter()

# Request and Response Models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Helper Functions
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Generate a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@router.post("/register", tags=["Authentication"])
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Add the new user to the database
    new_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # Add hashing in production
        balance=10000.00  # Initial balance
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "balance": new_user.balance}

@router.post("/login", response_model=Token, tags=["Authentication"])
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Login and generate a JWT token."""
    db_user = db.query(DBUser).filter(DBUser.email == login_request.email).first()
    if not db_user or db_user.hashed_password != login_request.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-token", tags=["Authentication"])
def verify_token(token: str):
    """Verify a JWT token."""
    decoded_data = decode_access_token(token)
    return {"decoded_data": decoded_data}
