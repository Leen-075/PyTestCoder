# app/models/post.py
# 帖子模块，作为论坛系统的核心模块，包含了帖子的基本信息，以及帖子的操作方法
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates  # 从 sqlalchemy.orm 导入 validates
from sqlalchemy.sql import func
from ..database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关联关系
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

    # 添加验证
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title is too long")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Content cannot be empty")
        return content