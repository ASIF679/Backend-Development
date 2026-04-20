from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# supabase url:::
DATABASE_URL = "postgresql://postgres.wuqtkcueogrvwhkxsazp:Test%40123679@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"
# SQLAlchemy engine setup with recommended pooling options
engine = create_engine(
    DATABASE_URL,    #Database connection string:::
    pool_pre_ping=True,      # Helps avoid stale connections
    pool_size=10,
    max_overflow=20,
    pool_timeout=30, #before providing errros wait for 30 seconds::
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
# Dependency for FastAPI route injection
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()