from pydantic import BaseModel

class OrderItemResponse(BaseModel):

    id: str
    order_id: str
    product_id: str
    quantity: int
    price: int

class OrderItemPostModel(BaseModel):

    order_id: str
    product_id: str
    quantity: int

class OrderItemUpdate(BaseModel):

    quantity: int