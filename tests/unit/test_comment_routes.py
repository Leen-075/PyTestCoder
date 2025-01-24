# tests/unit/test_comment_routes.py
import pytest
from app.models.comment import Comment
from app.models.post import Post

class TestCommentRoutes:
    def test_create_comment_success(self, client, test_token, test_db, test_user):
        """测试成功创建评论"""
        # 先创建一个帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 创建评论
        response = client.post(
            "/api/v1/comments/",
            json={
                "content": "Test Comment",
                "post_id": post.id
            },
            headers={"Authorization": f"Bearer {test_token}"}  # 添加认证token
        )
        assert response.status_code == 200
        data = response.json()
        assert data["content"] == "Test Comment"
        assert data["post_id"] == post.id

    def test_comment_without_auth(self, client, test_db, test_user):
        """测试未认证用户创建评论"""
        # 创建帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 尝试创建评论但不提供token
        response = client.post(
            "/api/v1/comments/",
            json={
                "content": "Test Comment",
                "post_id": post.id
            }
        )
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_invalid_auth_comment(self, client, test_db, test_user):
        """测试无效token创建评论"""
        # 创建帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 使用无效token尝试创建评论
        response = client.post(
            "/api/v1/comments/",
            json={
                "content": "Test Comment",
                "post_id": post.id
            },
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]