from pydantic import BaseModel

class ProductResponseModel(BaseModel):

    id: str
    name: str
    price: int
    description: str

class ProductPostModel(BaseModel):

    name: str
    price: int
    description: str