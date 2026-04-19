from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DatabaseURL = "Provide your Database url here !"
# Create the engine
engine = create_engine(DatabaseURL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
