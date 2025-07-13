# schemas/feedback.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class SubmissionMethod(str, Enum):
    WEB = "web"
    SMS = "sms"
    USSD = "ussd"
    IVR = "ivr"
    VOICE = "voice"

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class FeedbackBase(BaseModel):
    patient_id: Optional[str] = Field(None, example="PAT123")
    patient_name: str = Field(..., example="John Doe")
    age: int = Field(..., ge=0, example=30)
    gender: str = Field(..., example="Male", enum=["Male", "Female", "Other"])
    phone_number: Optional[str] = Field(None, example="+237670123456")
    condition: str = Field(..., example="Diabetes")
    treatment_satisfaction: int = Field(..., ge=1, le=5, example=4)
    communication_rating: int = Field(..., ge=1, le=5, example=4)
    facility_rating: int = Field(..., ge=1, le=5, example=4)
    overall_experience: int = Field(..., ge=1, le=5, example=4)
    recommendation_likelihood: int = Field(..., ge=1, le=5, example=5)
    comments: Optional[str] = Field(None, example="Good service")  # Renamed from content
    language: str = Field(..., example="french", enum=["english", "french", "douala", "bassa", "ewondo"])
    submission_method: SubmissionMethod = Field(..., example="web")
    sentiment: Optional[Sentiment] = Field(None, example="positive")
    audio_url: Optional[str] = Field(None, example="https://example.com/audio.mp3")  # Renamed from voice_data
    emoji_rating: Optional[str] = Field(None, example="😊")
    is_synced: bool = Field(False, example=False)

class FeedbackCreate(FeedbackBase):
    pass  # Inherits all fields for API creation

class FeedbackResponse(FeedbackBase):
    id: int = Field(..., example=1)
    feedback_date: datetime = Field(..., example="2025-07-14T00:00:00Z")  # Renamed from date_submitted
    processed: bool = Field(False, example=False)

    class Config:
        orm_mode = True
