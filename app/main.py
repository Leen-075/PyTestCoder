from fastapi import FastAPI
from .routes import user,post
from . import models
from .database import engine
#帖子功能
from .routes import post

app = FastAPI(title="PyTestCoder")

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(user.router)
app.include_router(post.router)  # 注册帖子路由