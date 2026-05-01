from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from database import get_user_from_db, SessionDep
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Annotated
from schemas import Token
import os

oauth2 = OAuth2PasswordBearer(tokenUrl="token")
crypt = pbkdf2_sha256
SECRET_KEYWORD = os.getenv("SECRET_KEYWORD")
ALGORITHM = os.getenv("ALGORITHM")

def hash_password(password: str):
    """Hashed normal password to store in db."""
    return crypt.hash(password)

def verify_password(password: str, hashed_password:str):
    """Verifies password with hashed password"""
    return crypt.verify(password, hashed_password)

def create_token(data: dict, expiry: timedelta= timedelta(minutes=30))->Token:
    """Generates a JWT access token with expiry"""
    expiry = datetime.now() + expiry
    data.update({"exp": expiry})
    jwt_token = jwt.encode(data, key=SECRET_KEYWORD, algorithm=[ALGORITHM])
    return Token(access_token=jwt_token)

def verify_token(token:Annotated[str,Depends(oauth2)]):
    """Verify user token and return user details"""
    try:
        data = jwt.decode(token=token, key=SECRET_KEYWORD, algorithms=[ALGORITHM])
        if not data:
            raise JWTError
        return data
    except ExpiredSignatureError:
        raise  HTTPException(440,"Session expired. Please login again.")

def authenticate_user(username: str, password: str, session:SessionDep) -> Token:
    """Authenticates user"""
    user = get_user_from_db(username, session)
    if not user:
        raise HTTPException(status_code = 401,detail="Invalid user details")
    verification = verify_password(password, user.hashed_password)
    if not verification:
        raise HTTPException(status_code= 401, detail="Invalid password")
    token = create_token(data = {"sub":username})
    if not token:
        raise HTTPException(status_code = 401,detail="Invalid user details")
    return token

def get_user_details(data: Annotated[dict, Depends(verify_token)]):
    """Validates user"""
    credentials_exception = HTTPException(401,"Could not validate user credentials")
    try:
        username = data.get("sub")
        if not username:
            raise credentials_exception
        return {"username":username}
    except JWTError :
        raise credentials_exception