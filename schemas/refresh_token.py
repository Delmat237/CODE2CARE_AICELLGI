# schemas/refresh_token.py
from sqlalchemy import Column, String, DateTime, Boolean
from database import Base
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    token = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)