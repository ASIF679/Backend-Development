from Database import engine, Base
from model import User, Blog, Comment
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
from sqlalchemy.orm import Session
from Database import engine
from model import User
from auth import hash_password 
db = Session(bind=engine)
