import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from app.models.user_model import UserBase, TokenData

# Secret key to encode/decode JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer is a class that provides the authentication scheme for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        email: str = payload.get("email")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid token or token expired")
        return UserBase(username=username, email=email)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid token")

def get_current_user(token: str) -> UserBase:
    UserBase = decode_access_token(token)
    return UserBase