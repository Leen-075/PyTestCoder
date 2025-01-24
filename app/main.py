# app/main.py
from fastapi import FastAPI
from .routes import user
from . import models
from .database import engine
from .core.config import API_V1_PREFIX
#帖子功能
from .routes import post
# 评论功能
from .routes import comment

app = FastAPI(title="PyTestCoder")

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 注册路由 - 添加API前缀
# app.include_router(user.router, prefix=API_V1_PREFIX)
# app.include_router(post.router, prefix=API_V1_PREFIX)
# app.include_router(comment.router, prefix=API_V1_PREFIX)
app.include_router(post.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(comment.router, prefix="/api/v1")
# 基础健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "healthy"}