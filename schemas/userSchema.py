from pydantic import BaseModel
from typing import Optional


class UserPostModel(BaseModel):

    username: str
    email: str
    password: str


class UserResponseModel(BaseModel):

    id: str
    username: str
    email: str
    full_name: Optional[str]
    address: Optional[str]
    phone_number: Optional[str]


    class Config:
        orm_mode = True
