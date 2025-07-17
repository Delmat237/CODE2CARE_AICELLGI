from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime, timezone

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, nullable=True)  # Link to Patient
    message = Column(String, nullable=False)
    language = Column(String, nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    channel = Column(String, nullable=False)  # e.g., "sms", "ivr", "email"
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc)) 
