from pydantic import BaseModel, Field


# ----- Item(예: 상품) -----
class ItemIn(BaseModel):
    # 클라이언트가 요청으로 보내는 데이터 형식
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., ge=0)  # 0 이상


class ItemOut(ItemIn):
    # 응답으로 돌려줄 때는 id를 같이 보냄
    id: int


# ----- User(예: 사용자) -----
class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str


class UserOut(UserIn):
    id: int
