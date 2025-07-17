from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from config.settings import settings
from pydantic import BaseModel
from typing import Optional
from schemas.user import User, UserResponse
from passlib.context import CryptContext
from schemas.refresh_token import RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class TokenData(BaseModel):
    username: Optional[str] = None
    role: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        
        # Get the full user from database
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise credentials_exception
            
        return UserResponse(
            username=user.username,
            email=user.email,  
            phone_number=user.phone_number,
            role=user.role
        )
    except JWTError:
        raise credentials_exception

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def create_refresh_token(data: dict, db: Session, expires_delta: Optional[timedelta] = None):
    expires_delta = expires_delta or timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = data.copy()
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    
    refresh_token = jwt.encode(to_encode, settings.REFRESH_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Store the refresh token in database
    db_refresh_token = RefreshToken(
        token=refresh_token,
        username=data["sub"],
        expires_at=expire
    )
    db.add(db_refresh_token)
    db.commit()
    
    return refresh_token

def validate_refresh_token(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # Check if token is revoked
        db_token = db.query(RefreshToken).filter(
            RefreshToken.token == token,
            RefreshToken.username == username,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.utcnow()
        ).first()
        
        if not db_token:
            raise credentials_exception
            
        return username
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )