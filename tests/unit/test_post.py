# 帖子功能测试
# tests/unit/test_post.py
# tests/unit/test_post.py
import pytest
from app.models import Post, Comment
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class TestPost:
    def test_create_post(self, test_db, test_user):
        """测试创建帖子"""
        post_data = {
            "title": "Test Post",
            "content": "Test Content",
            "user_id": test_user.id
        }
        
        post = Post(**post_data)
        test_db.add(post)
        test_db.commit()
        
        saved_post = test_db.query(Post).filter(Post.id == post.id).first()
        assert saved_post is not None
        assert saved_post.title == post_data["title"]
        assert saved_post.content == post_data["content"]
    
    def test_update_post(self, test_db, test_user):
        """测试更新帖子"""
        # 创建原始帖子
        post = Post(
            title="Original Title",
            content="Original Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()
        
        # 更新帖子
        post.title = "Updated Title"
        post.content = "Updated Content"
        test_db.commit()
        
        # 验证更新
        updated_post = test_db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.title == "Updated Title"
        assert updated_post.content == "Updated Content"
        assert updated_post.updated_at is not None  # 检查更新时间是否被设置
    
    def test_delete_post(self, test_db, test_user):
        """测试删除帖子"""
        # 创建帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()
        
        post_id = post.id
        
        # 删除帖子
        test_db.delete(post)
        test_db.commit()
        
        # 验证删除
        deleted_post = test_db.query(Post).filter(Post.id == post_id).first()
        assert deleted_post is None

    def test_delete_post_with_comments(self, test_db, test_user):
        """测试删除带有评论的帖子"""
        # 创建帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 添加评论
        comment = Comment(
            content="Test Comment",
            user_id=test_user.id,
            post_id=post.id
        )
        test_db.add(comment)
        test_db.commit()

        # 删除帖子
        test_db.delete(post)
        test_db.commit()

        # 验证帖子和评论都被删除
        assert test_db.query(Post).filter(Post.id == post.id).first() is None
        assert test_db.query(Comment).filter(Comment.post_id == post.id).first() is None

    def test_query_post_with_comments(self, test_db, test_user):
        """测试查询带有评论的帖子"""
        # 创建帖子
        post = Post(
            title="Test Post",
            content="Test Content",
            user_id=test_user.id
        )
        test_db.add(post)
        test_db.commit()

        # 添加多个评论
        comments = [
            Comment(content=f"Comment {i}", user_id=test_user.id, post_id=post.id)
            for i in range(3)
        ]
        test_db.add_all(comments)
        test_db.commit()

        # 查询帖子及其评论
        queried_post = test_db.query(Post).filter(Post.id == post.id).first()
        assert queried_post is not None
        assert len(queried_post.comments) == 3
        assert all(comment.post_id == post.id for comment in queried_post.comments)

    @pytest.mark.parametrize("title,content,expected_error", [
        ("", "Content", ValueError),           # 空标题
        ("Title", "", ValueError),             # 空内容
        ("A" * 101, "Content", ValueError),    # 标题过长
    ])
    def test_post_validation(self, test_db, test_user, title, content, expected_error):
        """测试帖子验证"""
        with pytest.raises(expected_error):
            post = Post(
                title=title,
                content=content,
                user_id=test_user.id
            )

    def test_post_ordering(self, test_db, test_user):
        """测试帖子排序"""
        # 创建多个帖子
        posts = [
            Post(
                title=f"Post {i}",
                content=f"Content {i}",
                user_id=test_user.id
            )
            for i in range(3)
        ]
        test_db.add_all(posts)
        test_db.commit()

        # 验证按创建时间降序排序
        ordered_posts = test_db.query(Post).order_by(Post.created_at.desc()).all()
        assert len(ordered_posts) == 3
        for i in range(len(ordered_posts)-1):
            assert ordered_posts[i].created_at >= ordered_posts[i+1].created_at