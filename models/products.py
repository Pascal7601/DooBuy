from core.baseModel import BaseModel
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship


class Product(BaseModel):
    """
    
    """

    __tablename__ = 'products'

    name = Column(String(20), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(30))

    #relationship
    orderItems = relationship('OrderItems', back_populates='product')