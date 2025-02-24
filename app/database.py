from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    print("All tables created")
    
init_db()















# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # SQLite database URL
# DATABASE_URL = "sqlite:///./trading.db"

# # Create the SQLite engine
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}
# )

# # Create a sessionmaker for managing database sessions
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class for ORM models
# Base = declarative_base()

# def init_db():
#     Base.metadata.create_all(bind=engine)
    
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
