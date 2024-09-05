from models.order_items import OrderItems
from models.orders import Order
from models.products import Product
from models.users import User
from baseModel import Base
from .database import engine

Base.metadata.create_all(bind=engine)