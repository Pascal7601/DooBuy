from core.connection import get_db
from fastapi import Depends, APIRouter, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from models.order_items import OrderItems
from schemas import orderItemSchema


order_items_router = APIRouter(prefix='/api/v1/order_items', tags=['order_items'])

@order_items_router.get('/', response_model=List[orderItemSchema.OrderItemResponse])
def all_orders(db: Session = Depends(get_db)):
    """
    get all products
    """
    order_items = db.query(OrderItems).all()
    return order_items


@order_items_router.get('/{order_item_id}', response_model=orderItemSchema.OrderItemResponse)
async def orders(order_item_id: str, db: Session = Depends(get_db)):
    """
    get user by their id
    """
    order_item = db.query(OrderItems).filter(OrderItems.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order not found')
    return order_item


@order_items_router.post('/', status_code=status.HTTP_201_CREATED)
async def add_order_item(order_item: orderItemSchema.OrderItemPostModel, db: Session = Depends(get_db)):
    """
    add a user
    """
    new_order_item = OrderItems(
        order_id = order_item.order_id,
        product_id=order_item.product_id,
        quantity = order_item.quantity)
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return {'message': f'succesfully added an order item order_item_id {new_order_item.id} to our system'}


@order_items_router.put('/{order_item_id}', response_model=orderItemSchema.OrderItemResponse)
async def update_order_item(order_item_id: str, updated_data: orderItemSchema.OrderItemUpdate,
                      db: Session = Depends(get_db)):
    """
    update a user
    """
    order_item = db.query(OrderItems).filter(OrderItems.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order item not found')
        
    order_item.quantity = updated_data.quantity
    db.commit()
    db.refresh(order_item)

    return order_item


@order_items_router.delete('/{order_item_id}')
async def remove_order_item(order_item_id: str, db: Session = Depends(get_db)):
    """
    cancel order by their id
    """
    order_item = db.query(OrderItems).filter(OrderItems.id == order_item_id).first()
    if not order_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'order item not found')
    db.delete(order_item)
    db.commit()
    return {'message': 'order item was succesfully removed'}