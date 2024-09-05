from core.baseModel import BaseModel
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Order(BaseModel):

    __tablename__ = 'orders'

    total = Column(Integer)
    user_id = Column(ForeignKey('users.id'))
    status = Column(String(20), default='pending')

    user = relationship('User', back_populates='orders')
    orderItems = relationship('OrderItems', back_populates='order', cascade='all, delete-orphan')