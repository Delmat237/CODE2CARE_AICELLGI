from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id = Column(String, ForeignKey("patients.external_id"), nullable=True)  # Lien vers patients
    message = Column(String, nullable=False)
    language = Column(String, nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    phone_number = Column(String, nullable=True)  # Changé en nullable=True
    email = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    channel = Column(String, nullable=False)  # e.g., "sms", "ivr", "email"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)