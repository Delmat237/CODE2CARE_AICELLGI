# routers/feedback.py
from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.feedback import Feedback  # SQLAlchemy model
from models.feedback import FeedbackCreate, FeedbackResponse  # Pydantic models
import base64
from google.cloud import speech
import os
from googletrans import Translator
from config.settings import settings
from utils.auth import get_current_user

router = APIRouter()

# Initialize Google Cloud Speech client safely
try:
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        # Use environment variable if set
        client = speech.SpeechClient()
    else:
        # Fall back to credentials file
        creds_path = os.path.join(os.path.dirname(__file__), "..", "google-credentials.json")
        credentials = service_account.Credentials.from_service_account_file(creds_path)
        client = speech.SpeechClient(credentials=credentials)
except Exception as e:
    client = None
    print(f"Warning: Failed to initialize SpeechClient - {str(e)}")


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    if not client:
        raise HTTPException(
            status_code=503,
            detail="Speech-to-text service currently unavailable"
        )
    
    db_feedback = Feedback(**feedback.dict(exclude_unset=True))
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    # Process voice data if provided
    if feedback.voice_data:
        try:
            audio_data = base64.b64decode(feedback.voice_data)
            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="fr-FR"
            )
            response = client.recognize(config=config, audio=audio)

            if response.results:
                transcribed_text = response.results[0].alternatives[0].transcript
                if feedback.language != "french" and feedback.language in ["douala", "bassa", "ewondo"]:
                    translated = translator.translate(transcribed_text, dest="french").text
                    db_feedback.comments = translated
                else:
                    db_feedback.comments = transcribed_text
                db_feedback.processed = True
            else:
                db_feedback.processed = False
                raise HTTPException(status_code=400, detail="Voice transcription failed")
        except Exception as e:
            db_feedback.processed = False
            db.commit()
            raise HTTPException(status_code=500, detail=f"Error processing voice data: {str(e)}")

    db.commit()
    return db_feedback

@router.get("", response_model=list[FeedbackResponse])
def get_all_feedback(db: Session = Depends(get_db)):
    feedback_list = db.query(Feedback).all()
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback found")
    return feedback_list

@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update_feedback(feedback_id: int, feedback_update: FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    update_data = feedback_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(db_feedback)
    db.commit()
    return {"message": "Feedback deleted successfully"}