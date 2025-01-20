from ./app.database import Base, engine
from ./app.models import User, Holding

# Drop all tables (optional, only if you're starting fresh)
Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")