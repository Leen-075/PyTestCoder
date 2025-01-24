# 用户认证测试
# tests/unit/test_auth.py
import pytest
from fastapi import HTTPException
from app.utils.auth import create_access_token, get_current_user
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data=data)
    
    # 验证token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload.get("sub") == "test@example.com"

async def test_get_current_user(client, test_token, test_db):
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200