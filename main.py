from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from models import ItemIn, ItemOut, UserIn, UserOut
from time import perf_counter

app = FastAPI(title="WSD REST API Assignment")

@app.middleware("http")
async def log_and_time(request: Request, call_next):
    start = perf_counter()
    print(f"[REQ] {request.method} {request.url.path}")  

    try:
        response: Response = await call_next(request)
    except Exception as e:
        duration_ms = int((perf_counter() - start) * 1000)
        print(f"[ERR] {request.method} {request.url.path} -> 500 ({duration_ms} ms): {e}")
        return err("Internal Server Error", code=500)

    duration_ms = int((perf_counter() - start) * 1000)
    response.headers["X-Process-Time-ms"] = str(duration_ms) 
    print(f"[RES] {request.method} {request.url.path} -> {response.status_code} ({duration_ms} ms)")
    return response

ITEMS: dict[int, ItemOut] = {}
USERS: dict[int, UserOut] = {}
_item_seq = 0
_user_seq = 0

def ok(data, code: int = 200):
    """
    성공 응답을 항상 같은 형식으로 보내기 위한 헬퍼
    {
      "status": "success",
      "data": ...
    }
    """
    return JSONResponse(status_code=code, content={"status": "success", "data": data})


def err(message: str, code: int):
    """
    에러 응답도 항상 같은 형식으로
    {
      "status": "error",
      "error": {
        "code": 404,
        "message": "Item not found"
      }
    }
    """
    return JSONResponse(
        status_code=code,
        content={"status": "error", "error": {"code": code, "message": message}},
    )

@app.post("/items", status_code=201)
async def create_item(payload: ItemIn):
    """
    새 Item(상품) 생성
    """
    global _item_seq

    _item_seq += 1  
    item = ItemOut(id=_item_seq, **payload.dict()) 
    ITEMS[item.id] = item  

    return ok(item.dict(), code=201)

@app.post("/users", status_code=201)
async def create_user(payload: UserIn):
    """
    새 User(사용자) 생성
    """
    global _user_seq

    _user_seq += 1
    user = UserOut(id=_user_seq, **payload.dict())
    USERS[user.id] = user

    return ok(user.dict(), code=201)

@app.put("/items/{item_id}")
async def replace_item(item_id: int, payload: ItemIn):
    """
    특정 Item 전체 수정
    """
    if item_id not in ITEMS:
        return err("Item not found", code=404)

    item = ItemOut(id=item_id, **payload.dict())
    ITEMS[item_id] = item

    return ok(item.dict(), code=200)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """
    특정 Item 삭제
    """
    if item_id not in ITEMS:
        return err("Item not found", code=404)

    del ITEMS[item_id]

    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=204, content={"status": "success", "data": None})

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """
    특정 User 삭제
    """
    if user_id not in USERS:
        return err("User not found", code=404)

    del USERS[user_id]

    return ok({"deleted": user_id}, code=200)

@app.put("/users/{user_id}")
async def replace_user(user_id: int, payload: UserIn):
    """
    특정 User 전체 수정
    """
    if user_id not in USERS:
        return err("User not found", code=404)

    user = UserOut(id=user_id, **payload.dict())
    USERS[user_id] = user

    return ok(user.dict(), code=200)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    특정 Item 하나 조회
    """
    item = ITEMS.get(item_id)
    if not item:
        return err("Item not found", code=404)

    return ok(item.dict(), code=200)

@app.get("/users")
async def list_users():
    """
    모든 User 조회
    """
    return ok([u.dict() for u in USERS.values()], code=200)

@app.get("/")
async def root():
    return {
        "status": "success",
        "data": "Hello, WSD!"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/_boom")
async def boom():
    """
    강제로 예외를 발생시켜 500 응답을 테스트
    """
    raise RuntimeError("forced error for 500 demo")


@app.get("/_unavailable")
async def unavailable():
    """
    503 Service Unavailable 응답 데모
    """
    return err("Service temporarily unavailable", code=503)