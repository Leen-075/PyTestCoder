# tests/unit/test_base.py
class TestBaseAPI:
    def test_api_root(self, client):
        """测试API根路径是否正常运行"""
        response = client.get("/api/v1/")
        # 由于我们没有定义根路径的处理，应该返回404
        assert response.status_code == 404

    def test_api_health(self, client):
        """测试API健康检查"""
        response = client.get("/health")
        assert response.status_code == 200