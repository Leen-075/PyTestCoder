# app/core/config.py
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

