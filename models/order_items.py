from core.baseModel import BaseModel
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship

class OrderItems(BaseModel):

    __tablename__ = 'orderItems'

    order_id = Column(String(150), ForeignKey('orders.id'), nullable=False)
    product_id = Column(String(150), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    #relationship
    order = relationship('Order', back_populates='orderItems')
    product = relationship('Product', back_populates='orderItems')

    @property
    def price(self):
        return self.product.price

