from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
# Constants
SECRET_KEY = "asif12345678"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 40 # in minutes
# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Hash a plain password
def hash_password(password: str):
    return pwd_context.hash(password)
# Verify a plain password against a hashed one
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
# Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# Decode and verify access token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

