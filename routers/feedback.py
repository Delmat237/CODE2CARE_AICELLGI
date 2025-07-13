from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.feedback import FeedbackCreate, FeedbackResponse
from schemas.feedback import Feedback
import base64

router = APIRouter()

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    # Placeholder for voice transcription (integrate Google Speech-to-Text here)
    if feedback.voice_data:
        db_feedback.processed = False  # Mark for async processing
        db.commit()
    return db_feedback