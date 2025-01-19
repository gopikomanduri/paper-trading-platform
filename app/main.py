from fastapi import FastAPI
from app.routes import auth, orders, transactions  # Import all route modules

# Create FastAPI instance
app = FastAPI(title="Algorithmic Trading Platform", version="1.0.0")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Algorithmic Trading Platform"}
