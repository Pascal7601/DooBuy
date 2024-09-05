from core.baseModel import Base
from core.database import engine
from fastapi import FastAPI


app = FastAPI()

from models.order_items import OrderItems
from models.orders import Order
from models.products import Product
from models.users import User


Base.metadata.create_all(bind=engine)

@app.get('/')
def home():
    return 'hello'

