# tests/unit/test_post_routes.py
import pytest
from app.models.post import Post
from app import models

class TestPostRoutes:
   def test_create_post_success(self, client, test_token):
       """测试成功创建帖子"""
       response = client.post(
           "/api/v1/posts/",
           json={
               "title": "Test Post",
               "content": "Test Content"
           },
           headers={"Authorization": f"Bearer {test_token}"}
       )
       assert response.status_code == 200
       data = response.json()
       assert data["title"] == "Test Post"
       assert data["content"] == "Test Content"

   @pytest.mark.skip(reason="暂时跳过删除验证的测试")
   def test_delete_post(self, client, test_token, test_db, test_user):
       """测试删除帖子"""
       post = models.Post(
           title="Test Post",
           content="Test Content",
           user_id=test_user.id
       )
       test_db.add(post)
       test_db.commit()

       # 保存post_id,因为post对象在删除后可能无法访问
       post_id = post.id
       response = client.delete(
           f"/api/v1/posts/{post_id}",
           headers={"Authorization": f"Bearer {test_token}"}
       )
       assert response.status_code == 204   

       

       # 验证删除是否成功
       # 使用保存的post_id来查询
       deleted_post = test_db.query(Post).filter(Post.id == post_id).first()
       assert deleted_post is None

   @pytest.mark.parametrize("post_data,expected_status", [
       ({"title": "", "content": "Content"}, 400),      # 空标题测试
       ({"title": "Title", "content": ""}, 400),        # 空内容测试
       ({"title": "A"*101, "content": "Content"}, 400)  # 标题过长测试
   ])
   def test_create_post_validation(self, client, test_token, post_data, expected_status):
       """测试帖子数据验证"""
       response = client.post(
           "/api/v1/posts/",
           json=post_data,
           headers={"Authorization": f"Bearer {test_token}"}
       )
       assert response.status_code == expected_status
       if expected_status == 400:
           assert "Could not create post" in response.json()["detail"]

   def test_update_post(self, client, test_token, test_db, test_user):
       """测试更新帖子"""
       # 创建帖子
       post = Post(
           title="Original Title",
           content="Original Content",
           user_id=test_user.id
       )
       test_db.add(post)
       test_db.commit()

       # 更新帖子
       response = client.put(
           f"/api/v1/posts/{post.id}",
           json={
               "title": "Updated Title",
               "content": "Updated Content"
           },
           headers={"Authorization": f"Bearer {test_token}"}
       )
       assert response.status_code == 200
       data = response.json()
       assert data["title"] == "Updated Title"
       assert data["content"] == "Updated Content"

   def test_get_nonexistent_post(self, client):
       """测试获取不存在的帖子"""
       response = client.get("/api/v1/posts/999")
       assert response.status_code == 404

   def test_get_post(self, client, test_db, test_user):
       """测试获取存在的帖子"""
       # 创建帖子
       post = Post(
           title="Test Post",
           content="Test Content",
           user_id=test_user.id
       )
       test_db.add(post)
       test_db.commit()

       # 获取帖子
       response = client.get(f"/api/v1/posts/{post.id}")
       assert response.status_code == 200
       data = response.json()
       assert data["title"] == "Test Post"
       assert data["content"] == "Test Content"

   def test_update_nonexistent_post(self, client, test_token):
       """测试更新不存在的帖子"""
       response = client.put(
           "/api/v1/posts/999",
           json={
               "title": "Updated Title",
               "content": "Updated Content"
           },
           headers={"Authorization": f"Bearer {test_token}"}
       )
       assert response.status_code == 404