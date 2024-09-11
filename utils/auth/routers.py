from core.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter
from models.users import User
from models.orders import Order
from schemas.orderSchema import OrderResponseModel
from .schemas import UserSignInPostModel
from schemas.userSchema import UserResponseModel
from typing import List
from utils.auth.auth import verify_password, create_token, decode_token, authenticate_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from .auth import expiry


auth = APIRouter(prefix='/api/v1/auth', tags=['auth'])

security = HTTPBearer()


@auth.post('/token')
def generate_token(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(email, password, db)
    token = create_token({"sub": user.email})
    response = JSONResponse(content={"access_token": token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=expiry * 30)
    return response


@auth.get('/sign_in')
def sign_in(email: str, password: str, db: Session = Depends(get_db)):
    """
    sign in route for user
    """
    if not email or not password:
        return {"message": "please provide email and password"}
    
    user_1 = db.query(User).filter(User.email == email).first()
    if not user_1:
        return {"message": "user not found"}
    
    check_pwd = verify_password(password, user_1.hashed_password)
    if not check_pwd:
        return {"message": "wrong password, try again"}
    
    return {"messge": f"success {user_1.username} has succesfully logged in"}


@auth.get('/users/me', response_model=UserResponseModel)
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    determine current user
    """
    token = credentials.credentials
    payload = decode_token(token)
    user_email = payload.get("sub") 
    if user_email is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='user not authenticated')
    user = db.query(User).filter(User.email == user_email).first()
    return user

@auth.get('/user/orders', response_model=List[OrderResponseModel])
def get_user_orders(credentials: HTTPAuthorizationCredentials = Depends(security),
                    db: Session = Depends(get_db)):
    """
    get user's personal orders
    """
    token = credentials.credentials
    payload = decode_token(token)
    user_email = payload.get("sub")
    user = db.query(User).filter(User.email == user_email).first()
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders

    
    
    