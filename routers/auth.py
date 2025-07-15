# routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from database import get_db
from utils.auth import authenticate_user, create_access_token, get_current_user,create_refresh_token,validate_refresh_token
from pydantic import BaseModel
from datetime import timedelta
from config.settings import settings
from schemas.user import User, pwd_context  # For database model and hashing
from schemas.user import LoginRequest, RegisterRequest,TokenResponse,UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas.refresh_token import RefreshToken  # Import the RefreshToken model

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
          db=db  
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserResponse)
async def register(
    register_request: RegisterRequest, 
    db: Session = Depends(get_db)
):
    # Validation checks
    if db.query(User).filter(User.username == register_request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if db.query(User).filter(User.email == register_request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    if register_request.phone_number and db.query(User).filter(
        User.phone_number == register_request.phone_number
    ).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")


    # Create user
    hashed_password = pwd_context.hash(register_request.password)
    db_user = User(
        username=register_request.username,
        email=register_request.email,
        hashed_password=hashed_password,
        phone_number=register_request.phone_number,
        role=register_request.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    username = validate_refresh_token(refresh_token)
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user or inactive account"
        )
    
    # Invalidate old refresh token
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).update({"is_revoked": True})
    
    # Create new tokens
    new_access_token = create_access_token(data={"sub": user.username, "role": user.role})
    new_refresh_token = create_refresh_token(data={"sub": user.username},  db=db  )
    
    db.commit()
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.username == current_user["username"]
    ).first()
    
    if db_token:
        db_token.is_revoked = True
        db.commit()
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user