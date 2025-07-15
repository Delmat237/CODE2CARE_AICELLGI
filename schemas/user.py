from pydantic import BaseModel,EmailStr,validator
from sqlalchemy import Column, Integer, String, Boolean
from passlib.context import CryptContext
from database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    username: str
    password: str
    # email and phone_number not required for login

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    phone_number: str = None  # Optional as per the model
    password: str
    role: str = "user"  # e.g., "admin" or "user", to be validated

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

# Response Models
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    username: str
    email: str
    phone_number: str = None  
    role: str


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., "admin" or "user"
    is_active = Column(Boolean, default=True, nullable=False)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

