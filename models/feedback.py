from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    patient_id: str = Field(..., example="PAT123")
    language: str = Field(..., example="french", enum=["english", "french", "douala", "bassa", "ewondo"])
    content: Optional[str] = Field(None, example="Good service")
    rating: Optional[int] = Field(None, ge=1, le=5, example=4)
    voice_data: Optional[str] = Field(None, example="base64_encoded_audio")

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    date_submitted: datetime
    processed: bool = False

    class Config:
        orm_mode = True