# importing all the Packages:::
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Database import get_db
from auth import decode_access_token
from model import User
# setting up the token reader::::

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from Database import get_db
from auth import decode_access_token
from model import User

# Token extractor — looks for Authorization: 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# Get the currently logged-in user (from token)
def get_current_user(token=Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token plz refresh or recheck")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
# Allow any logged-in user (admin or not)
def require_user(current_user=Depends(get_current_user)):
    return current_user
# Allow only admins
def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin access only"
        )
    return current_user
