# tests/unit/test_user_routes.py
import pytest
from datetime import timedelta
import time
from app.utils.auth import create_access_token
from app import models

# 用户认证测试类
class TestAuthentication:
    def test_no_token(self, client):
        """测试没有token的情况"""
        response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Test Post",
                "content": "Test Content"
            }
        )
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_invalid_token_format(self, client):
        """测试格式错误的token"""
        response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Test Post",
                "content": "Test Content"
            },
            headers={"Authorization": "NotBearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_expired_token(self, client):
        """测试过期的token"""
        # 创建一个过期的token
        expired_token = create_access_token(
            data={"sub": "test@example.com"},
            expires_delta=timedelta(microseconds=1)
        )
        time.sleep(1)  # 等待token过期

        response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Test Post",
                "content": "Test Content"
            },
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]

# 用户基本功能测试类
class TestUserRoutes:
    def test_user_registration_success(self, client):
        """测试用户成功注册"""
        response = client.post(
            "/api/v1/users/",
            json={
                "username": "testuser1",
                "email": "test1@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "testuser1"
        assert data["email"] == "test1@example.com"
        assert "id" in data

    def test_user_login_success(self, client):
        """测试用户成功登录"""
        # 先注册用户
        client.post(
            "/api/v1/users/",
            json={
                "username": "testuser1",
                "email": "test1@example.com",
                "password": "password123"
            }
        )
        
        # 测试登录
        response = client.post(
            "/api/v1/users/login",
            data={
                "username": "test1@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_user_login_wrong_password(self, client):
        """测试错误密码登录"""
        # 先注册用户
        client.post(
            "/api/v1/users/",
            json={
                "username": "testuser1",
                "email": "test1@example.com",
                "password": "password123"
            }
        )
        
        # 使用错误密码登录
        response = client.post(
            "/api/v1/users/login",
            data={
                "username": "test1@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]