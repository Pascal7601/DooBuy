from pydantic import BaseModel

class UserSignInPostModel(BaseModel):

    email: str
    password: str