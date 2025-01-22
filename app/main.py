from fastapi import FastAPI
from .routes import user
from . import models
from .database import engine

app = FastAPI(title="PyTestCoder")

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(user.router)