from core.baseModel import Base
from core.database import engine
from fastapi import FastAPI
from routers import users, products, orders, order_items
from utils.auth import routers

from models.order_items import OrderItems
from models.orders import Order
from models.products import Product
from models.users import User

app = FastAPI()

app.include_router(users.router)
app.include_router(products.products_router)
app.include_router(routers.auth)
app.include_router(orders.orders_router)
app.include_router(order_items.order_items_router)


Base.metadata.create_all(bind=engine)

@app.get('/')
def home():
    return 'hello'

