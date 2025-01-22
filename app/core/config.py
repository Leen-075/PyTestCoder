# app/core/config.py
from datetime import timedelta

# API 配置
API_V1_PREFIX = "/api/v1"
# 配置信息
# 开发测试环境中使用固定密钥
# 在生产环境中应该：
# 1. 使用环境变量：SECRET_KEY = os.getenv("SECRET_KEY")
# 2. 使用配置管理系统
# 3. 定期轮换密钥
# JWT 配置
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30