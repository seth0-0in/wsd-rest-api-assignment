# WSD REST API Assignment

전북대학교 **웹서비스설계** 수업 REST API 실습 과제입니다.  
FastAPI 기반으로 아이템(Item) / 사용자(User) 관리 기능을 구현했습니다.

---

## 1. 기술 스택
- **Python 3.11+**
- **FastAPI**
- **Uvicorn**

---

## 2. 실행 방법

```bash
# 1) 가상환경 생성 (선택)
python -m venv .venv
.venv\Scripts\activate   # Windows

# 2) 패키지 설치
pip install -r requirements.txt

# 3) 서버 실행
python -m uvicorn main:app --reload

# 4) 접속 주소
# - API 문서: http://127.0.0.1:8000/docs
# - Root:     http://127.0.0.1:8000/
```

---

## 3. API 목록

### Items
| Method | Path          | 설명             |
|--------|---------------|------------------|
| POST   | `/items`      | 아이템 생성      |
| GET    | `/items/{id}` | 특정 아이템 조회 |
| PUT    | `/items/{id}` | 특정 아이템 수정 |
| DELETE | `/items/{id}` | 특정 아이템 삭제 |

### Users
| Method | Path          | 설명              |
|--------|---------------|-------------------|
| POST   | `/users`      | 사용자 생성       |
| GET    | `/users`      | 전체 사용자 조회  |
| PUT    | `/users/{id}` | 특정 사용자 수정  |
| DELETE | `/users/{id}` | 특정 사용자 삭제  |

---

## 4. 응답 형식

### 성공 응답 (2xx)
```json
{
  "status": "success",
  "data": { ... }
}
```

### 에러 응답 (4xx / 5xx)
```json
{
  "status": "error",
  "error": {
    "code": 404,
    "message": "Item not found"
  }
}
```
