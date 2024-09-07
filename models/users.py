from core.baseModel import BaseModel
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

class User(BaseModel):
    """
    User class
    """

    __tablename__ = 'users'

    username = Column(String(40), unique=True, nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    full_name = Column(String(40))
    hashed_password = Column(String(150), nullable=False)
    phone_number = Column(String(20))
    address = Column(Text)

    #relationship
    orders = relationship('Order', back_populates='user')
