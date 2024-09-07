from core.connection import get_db
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from models.orders import Order
from schemas import orderSchema


orders_router = APIRouter(prefix='/api/v1/orders', tags=['orders'])

@orders_router.get('/', response_model=List[orderSchema.OrderResponseModel])
def all_orders(db: Session = Depends(get_db)):
    """
    get all products
    """
    orders = db.query(Order).all()
    return orders


@orders_router.get('/{order_id}', response_model=orderSchema.OrderResponseModel)
async def orders(order_id: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order not found')
    return order


@orders_router.post('/', status_code=status.HTTP_201_CREATED)
async def place_order(order: orderSchema.OrderPostModel, db: Session = Depends(get_db)):
    """
    add a user
    """
    new_order = Order(
        user_id = order.user_id,
        total=order.total)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {'message': f'succesfully placed an order order_id {new_order.id} to our system'}


@orders_router.put('/{order_id}', response_model=orderSchema.OrderResponseModel)
async def update_order(order_id: str, updated_data: orderSchema.OrderUpdateModel,
                      db: Session = Depends(get_db)):
    """
    update a user
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order not found')
        
    if order.total:
        order.total = updated_data.total
    if order.status:
        order.status = updated_data.status
    db.commit()
    db.refresh(order)

    return order


@orders_router.delete('/{order_id}')
async def cancel_order(order_id: str, db: Session = Depends(get_db)):
    """
    cancel order by their id
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order not found')
    db.delete(order)
    db.commit()
    return {'message': 'order was succesfully cancelled'}