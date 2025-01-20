from app.database import Base, engine
from app.models import User, Holding
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import registry

# Drop all tables (optional, only if you're starting fresh)
Base.metadata.drop_all(bind=engine)


mapper_registry = registry()
mapper_registry.configure()

configure_mappers() 

# Create all tables
Base.metadata.create_all(bind=engine)
 

print("Tables created successfully.")