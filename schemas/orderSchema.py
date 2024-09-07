from pydantic import BaseModel


class OrderPostModel(BaseModel):
    total: int
    user_id: str

class OrderResponseModel(BaseModel):

    id: str
    total: int
    user_id: str
    status: str

class OrderUpdateModel(BaseModel):

    total: int
    status: str