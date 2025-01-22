from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/", response_model=schemas.PostOut)
def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(get_db)):

    # 首先查询确保用户存在
    user = db.query(models.User).first()  # 获取第一个用户用于测试
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found. Please create a user first"
        )
    
    # 临时使用固定的用户ID进行测试
    db_post = models.Post(
        **post.model_dump(),
        user_id=user.id #假设ID为1的用户存在
    )
    db.add(db_post)
    try:
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as e:
        db.rollback()
        # 添加日志或使用异常信息
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create post: {str(e)}"  # 使用异常信息
        )
    return db_post

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts