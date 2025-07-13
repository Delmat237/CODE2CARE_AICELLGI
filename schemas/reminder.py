from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    message = Column(String)
    language = Column(String)
    scheduled_time = Column(DateTime)
    phone_number = Column(String)
    status = Column(String, default="pending")