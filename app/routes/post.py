# app/routes/post.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging  # 添加日志
from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user
from fastapi.params import Query
from ..models import Post

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/", response_model=schemas.PostOut)
async def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        # 移除多余的用户查询，因为 current_user 已经包含了用户信息
        db_post = models.Post(
            **post.model_dump(),
            user_id=current_user.id
        )
        logger.info(f"Creating post: {post.model_dump()}")
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create post: {str(e)}"
        )

# 获取单个帖子
@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

# 修改更新帖子的函数，修正逻辑顺序
@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    post_update: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 先查找帖子
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # 然后检查权限
    if db_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # 更新帖子信息
    for var, value in post_update.model_dump().items():
        setattr(db_post, var, value)
    
    try:
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not update post: {str(e)}"
        )

# 添加认证到删除帖子的接口
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # 添加权限检查
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        db.delete(post)
        db.commit()
        return {"detail": "Post deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not delete post: {str(e)}"
        )
    

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取帖子列表"""
    posts = db.query(models.Post)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return posts

@router.get("/search", response_model=List[schemas.PostOut])
async def search_posts(
    db: Session = Depends(get_db),
    keyword: str = Query(None)
):
    """搜索帖子"""
    query = db.query(models.Post)
    
    if keyword:
        query = query.filter(
            models.Post.title.ilike(f"%{keyword}%") |
            models.Post.content.ilike(f"%{keyword}%")
        )
    
    return query.all()