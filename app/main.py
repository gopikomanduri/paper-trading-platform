from fastapi import FastAPI
from app.routes import auth, orders, transactions  # Import all route modules
from app.database import init_db
from sqlalchemy.orm import configure_mappers
from fastapi.middleware.cors import CORSMiddleware



# Create FastAPI instance
app = FastAPI(title="Algorithmic Trading Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.on_event("startup")
def startup_event():
    init_db()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Algorithmic Trading Platform"}

