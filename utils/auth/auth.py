from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from datetime import timedelta, datetime
from passlib.context import CryptContext
from core.connection import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.users import User



load_dotenv()

secret_key = os.getenv('SECRET_KEY')
algo = os.getenv('ALGORITHM')
expiry = int(os.getenv('EXPIRY_TIME'))


def create_token(data: dict):
    """
    create a jwt token
    """
    copy = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    copy.update({"exp": expire})
    encoded_token = jwt.encode(copy, secret_key, algorithm=algo)
    return encoded_token


def decode_token(token: str):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algo])
        return decoded
    except JWTError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid token')

#password hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_password_hash(password: str):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
    """
    verifies a user before logging in
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='user not found')
    if not verify_password(password, User.hashed_password):
        return {"message": "wrong password"}
    return user

    