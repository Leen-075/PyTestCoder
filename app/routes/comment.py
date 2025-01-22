from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

@router.post("/", response_model=schemas.CommentOut)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    # 验证帖子是否存在
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # 临时使用第一个用户（后面会加入认证）
    user = db.query(models.User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user found"
        )

    db_comment = models.Comment(
        **comment.model_dump(),
        user_id=user.id
    )
    
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Could not create comment: {str(e)}"
        )

@router.get("/post/{post_id}", response_model=List[schemas.CommentOut])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id
    ).all()
    return comments