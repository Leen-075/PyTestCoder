# tests/integration/test_user_post_flow.py
import pytest
from app import models

class TestUserPostFlow:
    def test_complete_user_flow(self, client):
        """测试完整用户流程：注册->登录->发帖->评论"""
        # 1. 用户注册
        register_response = client.post(
            "/api/v1/users/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert register_response.status_code == 201
        assert register_response.json()["email"] == "test@example.com"

        # 2. 用户登录
        login_response = client.post(
            "/api/v1/users/login",
            data={
                "username": "test@example.com",
                "password": "password123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        assert token is not None

        # 3. 创建帖子
        post_response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Test Post",
                "content": "Test Content"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert post_response.status_code == 200
        post_id = post_response.json()["id"]
        
        # 4. 验证帖子
        get_post_response = client.get(f"/api/v1/posts/{post_id}")
        assert get_post_response.status_code == 200
        assert get_post_response.json()["title"] == "Test Post"

        # 5. 发表评论
        comment_response = client.post(
            "/api/v1/comments/",
            json={
                "content": "Test Comment",
                "post_id": post_id
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert comment_response.status_code == 200
        assert comment_response.json()["content"] == "Test Comment"

    def test_post_with_comments_flow(self, client):
        """测试帖子和评论的完整流程"""
        # 1. 注册两个用户
        users = []
        for i in range(2):
            register_response = client.post(
                "/api/v1/users/",
                json={
                    "username": f"testuser{i}",
                    "email": f"test{i}@example.com",
                    "password": "password123"
                }
            )
            assert register_response.status_code == 201
            
            # 登录并获取token
            login_response = client.post(
                "/api/v1/users/login",
                data={
                    "username": f"test{i}@example.com",
                    "password": "password123"
                }
            )
            assert login_response.status_code == 200
            users.append({
                "email": f"test{i}@example.com",
                "token": login_response.json()["access_token"]
            })

        # 2. 第一个用户创建帖子
        post_response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Discussion Post",
                "content": "Let's discuss this topic"
            },
            headers={"Authorization": f"Bearer {users[0]['token']}"}
        )
        assert post_response.status_code == 200
        post_id = post_response.json()["id"]

        # 3. 两个用户都发表评论
        for user in users:
            comment_response = client.post(
                "/api/v1/comments/",
                json={
                    "content": f"Comment from {user['email']}",
                    "post_id": post_id
                },
                headers={"Authorization": f"Bearer {user['token']}"}
            )
            assert comment_response.status_code == 200

        # 4. 获取帖子的所有评论
        comments_response = client.get(f"/api/v1/comments/post/{post_id}")
        assert comments_response.status_code == 200
        comments = comments_response.json()
        assert len(comments) == 2

    def test_error_handling_flow(self, client):
        """测试错误处理流程"""
        # 1. 尝试使用已注册的邮箱注册
        register_response = client.post(
            "/api/v1/users/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert register_response.status_code == 201

        # 尝试重复注册
        duplicate_response = client.post(
            "/api/v1/users/",
            json={
                "username": "testuser2",
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert duplicate_response.status_code == 400

        # 2. 尝试使用错误密码登录
        wrong_login_response = client.post(
            "/api/v1/users/login",
            data={
                "username": "test@example.com",
                "password": "wrongpassword"
            }
        )
        assert wrong_login_response.status_code == 401