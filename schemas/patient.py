from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Link to User if authenticated
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    registration_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)