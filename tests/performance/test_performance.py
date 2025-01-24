# tests/performance/test_performance.py
import pytest
import time
from app.models import Post, Comment

class TestPerformance:
    def test_post_list_performance(self, client, test_db, test_user):
        """测试帖子列表加载性能"""
        # 批量创建帖子
        posts = [
            Post(
                title=f"Post {i}",
                content=f"Content {i}",
                user_id=test_user.id
            )
            for i in range(100)  # 创建100个帖子
        ]
        test_db.add_all(posts)
        test_db.commit()

        # 测试列表加载时间
        start_time = time.time()
        response = client.get("/api/v1/posts/")
        end_time = time.time()

        assert response.status_code == 200
        assert end_time - start_time < 1.0  # 响应时间应小于1秒

    def test_comment_query_performance(self, client, test_db, test_user):
        """测试评论查询性能"""
        # 创建一个帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 为帖子创建100条评论
        comments = [
            Comment(
                content=f"Comment {i}",
                post_id=post.id,
                user_id=test_user.id
            )
            for i in range(100)
        ]
        test_db.add_all(comments)
        test_db.commit()

        # 测试评论加载时间
        start_time = time.time()
        response = client.get(f"/api/v1/comments/post/{post.id}")
        end_time = time.time()

        assert response.status_code == 200
        assert end_time - start_time < 1.0  # 响应时间应小于1秒

    