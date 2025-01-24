# app/utils/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta,timezone
from typing import Optional
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

# 创建访问令牌
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        logger.info(f"Creating token with data: {to_encode}")  # 添加日志
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Created token: {encoded_jwt}")  # 添加日志
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise e


# 获取当前用户
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    logger.info(f"Received token: {token}")  # 添加日志
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded payload: {payload}")  # 添加日志

        email: str = payload.get("sub")
        logger.info(f"Extracted email: {email}")    # 添加日志
        
        if email is None:
            logger.error("No email found in token")
            raise credentials_exception
        

        user = db.query(models.User).filter(models.User.email == email).first()
        logger.info(f"Found user: {user is not None}")  # 添加日志

        if user is None:
            logger.error("User not found in database")
            raise credentials_exception
        return user
    
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")  # 添加错误日志
        raise credentials_exception
        
    
