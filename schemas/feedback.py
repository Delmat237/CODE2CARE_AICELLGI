from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from sqlalchemy.sql import func
from typing import Optional
from enum import Enum
from database import Base
from sqlalchemy.orm import relationship

class SubmissionMethod(Enum):
    WEB = "web"
    SMS = "sms"
    USSD = "ussd"
    IVR = "ivr"
    VOICE = "voice"

class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String, nullable=True)
    patient_name = Column(String, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    condition = Column(String, nullable=False)
    treatment_satisfaction = Column(Integer, nullable=False)
    communication_rating = Column(Integer, nullable=False)
    facility_rating = Column(Integer, nullable=False)
    overall_experience = Column(Integer, nullable=False)
    recommendation_likelihood = Column(Integer, nullable=False)
    feedback_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    comments = Column(String, nullable=False)
    language = Column(String, nullable=False)
    submission_method = Column(String, nullable=False)  # Store as string, validated by enum
    sentiment = Column(String, nullable=True)  # Store as string, validated by enum
    audio_url = Column(String, nullable=True)
    emoji_rating = Column(String, nullable=True)
    is_synced = Column(Boolean, default=False, nullable=False)

