from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)  # Link to Patient
    message = Column(String, nullable=False)
    language = Column(String, nullable=False)
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    status = Column(String, default="pending", nullable=False)
    channel = Column(String, nullable=False)  # e.g., "sms", "ivr", "email"
    patient = relationship("Patient", backref="reminders")