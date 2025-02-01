# tests/security/test_security.py
class TestSecurity:
    def test_authentication_security(self, client):
        """测试认证安全性"""
        # 测试无效 token
        response = client.get(
            "/api/v1/posts/",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert "Could not validate credentials" in response.json()["detail"]

    def test_xss_prevention(self, client, test_token):
        """测试 XSS 防护"""
        xss_payload = "<script>alert('xss')</script>"
        response = client.post(
            "/api/v1/posts/",
            json={
                "title": "Test Post",
                "content": xss_payload
            },
            headers={"Authorization": f"Bearer {test_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        # 验证内容已被转义
        assert "&lt;script&gt;" in data["content"]
        assert xss_payload not in data["content"]