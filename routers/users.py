from core.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter
from models.users import User
from schemas import userSchema
from typing import List
from utils.auth.auth import get_password_hash
from notifications.emails import send_registration_email


router = APIRouter(prefix='/api/v1', tags=['users'])

@router.get('/users', response_model=List[userSchema.UserResponseModel])
async def all_users(db: Session = Depends(get_db)):
    """
    
    """
    users = db.query(User).all()
    return users


@router.get('/users/{email}', response_model=userSchema.UserResponseModel)
async def user(email: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
    return user


@router.post('/users/', status_code=status.HTTP_201_CREATED)
async def add_user(user: userSchema.UserPostModel, db: Session = Depends(get_db)):
    """
    add a user
    """
    hash_pwd = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # send_registration_email(user.email, user.username) #only in production
    return {'message': f'succesfully registered user_id {new_user.id} to our system, kindly check your email'}


@router.put('/users/{email}', response_model=userSchema.UserResponseModel)
async def update_user(email: str, updated_data: userSchema.UserPostModel,
                      db: Session = Depends(get_db)):
    """
    update a user
    """
    user = await db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
        
    if user.username:
        user.username = updated_data.username
    if user.email:
        user.email = updated_data.email
    if user.hashed_password:
        user.hashed_password = updated_data.password
    db.commit()
    db.refresh(user)

    return user


@router.delete('/users/{email}')
async def delete_user(email: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'user not found')
    db.delete(user)
    db.commit()
    return {'message': 'user succesfully deleted'}





