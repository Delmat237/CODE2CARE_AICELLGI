from pydantic import BaseModel, Field
from datetime import datetime

class RefreshTokenBase(BaseModel):
    token: str = Field(..., example="abc123xyz")
    username: str = Field(..., example="john_doe")
    expires_at: datetime = Field(..., example="2025-07-14T10:00:00")        
    is_revoked: bool = Field(default=False, example=False)

class RefreshTokenCreate(RefreshTokenBase):
    pass
