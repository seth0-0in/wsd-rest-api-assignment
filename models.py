from pydantic import BaseModel, Field

class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., ge=0)  

class ItemOut(ItemIn):
    id: int

class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str

class UserOut(UserIn):
    id: int