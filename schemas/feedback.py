from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String, index=True)
    language = Column(String)
    content = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    voice_data = Column(String, nullable=True)
    date_submitted = Column(DateTime, default=lambda: datetime.utcnow())
    processed = Column(Boolean, default=False)