# 用户相关的验证模型
# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr  # 改成 EmailStr 来验证邮箱格式

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True  # 新版本 Pydantic 使用 from_attributes 替代 orm_mode

# 实现登录功能
class UserLogin(BaseModel):
    email: EmailStr  # 这里也改成 EmailStr
    password: str