from fastapi import FastAPI, Depends
from app.models.user_model import UserBase
from app.utils.jwt_utility import create_access_token, get_current_user
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Security, Depends, APIRouter

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login")
async def login(username: str, password: str):
    """
    Handles user login.

    Returns an access token if the credentials are valid. The access token
    can be used to access protected endpoints.

    Raises an HTTPException with status code 401 if the credentials are
    invalid.
    """
    if username == "testuser" and password == "testpassword":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username, "email": "test@email.com"}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/secure-endpoint/")
async def secure_endpoint(current_user: UserBase = Depends(get_current_user)):
    """
    This endpoint is only accessible if you have a valid access token.

    Use the login endpoint to obtain an access token, then use that token to access
    this endpoint.

    This endpoint will return a simple message with your username.
    """
    return {"message": f"Hello, {current_user.username}. This is a secure endpoint."}