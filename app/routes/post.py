from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging  # 添加日志
from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user

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
        # 首先查询确保用户存在
        user = db.query(models.User).first()
        logger.info(f"Found user: {user}")  # 记录用户信息
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No user found. Please create a user first"
            )
        
   # 创建帖子
        db_post = models.Post(
            **post.model_dump(),
            user_id=current_user.id
        )
        logger.info(f"Creating post: {post.model_dump()}")  # 记录帖子信息
        
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    
    except Exception as e:
        logger.error(f"Error creating post: {str(e)}")  # 记录错误
        db.rollback()
        # 添加日志或使用异常信息
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create post: {str(e)}"  # 使用异常信息
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

# 更新帖子
@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    post_update: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 检查是否是帖子作者
    if db_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # 查找帖子
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
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

# 删除帖子
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # 查找帖子
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
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