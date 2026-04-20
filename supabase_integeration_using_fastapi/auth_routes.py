import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from auth_utils import verify_supabase_token

load_dotenv()

router = APIRouter()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_KEY")  # Use anon/public key

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("Missing Supabase environment variables. Check .env file.")

class RegisterCredentials(BaseModel):
    email: EmailStr
    password: str
    username: str

class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register_user(user: RegisterCredentials):
    url = f"{SUPABASE_URL}/auth/v1/signup"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "email": user.email,
        "password": user.password,
        "options": {
            "data": {
                "username": user.username
            },
            "email_redirect_to": "http://localhost:8000/confirm"  # Optional confirmation redirect
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.post("/login")
def login_user(user: LoginCredentials):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {
        "apikey": SUPABASE_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "email": user.email,
        "password": user.password
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()  # access_token, refresh_token, etc.

@router.get("/verify-token")
def verify_token_route(user_id: str = Depends(verify_supabase_token)):
    return {
        "message": "Token is valid.",
        "user_id": user_id
    }
@router.get("/confirm")
def confirm_email_redirect():
    return {"message": "Email confirmed. You can now log in."}
