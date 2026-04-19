from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text 
from Database import get_db, engine, Base
# importing the tables from the Database:::
from model import User, Blog, Comment 
from typing import Annotated
from swagger_ui_configuration import custom_openapi
# importing the from auth::: JWT 
from auth import hash_password , verify_password , create_access_token , decode_access_token
from pydantic import BaseModel , EmailStr
from datetime import timedelta
from auth import ACCESS_TOKEN_EXPIRE_TIME    #Set the expires Time to 40 min 
# impoorting the dependcies to verify and get user :::
from dependencies import require_admin , require_user
# using the user routes from user_routes.py:::
from user_routes import router as user_route 
# importing the admin routes from admin.py:::
from admin_routes import router as admin_routes

app = FastAPI()
# Create tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")

@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.get("/healthcheck")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "Database connected successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
app.openapi = lambda: custom_openapi(app)  #setting up the custome wager UI ::::
# Correct Pydantic schema for the registering new_userss::
class CreateUser(BaseModel):
    username: str
    password: str
    email: EmailStr
# creating the Pydantic Schema for the user Login
class LoginUser(BaseModel):
    username: str
    password: str

# User register Function
@app.post("/register_user")
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    # Hash the password
    hashed_pwd = hash_password(user.password)
    # Create new user object
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd
    )
    # Save to DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

# User_login_Function:::::
@app.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)

    #dd is_admin to the token payload
    token = create_access_token(
        data={
            "sub": db_user.username,
            "is_admin": db_user.is_admin  
        },
        expires_delta=access_token_expires
    )
    return {"access_token": token, "token_type": "bearer"}

# calling the user_routes_function:: from user_route.py
app.include_router(user_route)
app.include_router(admin_routes)