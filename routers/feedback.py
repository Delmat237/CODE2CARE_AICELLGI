from fastapi import APIRouter, HTTPException, Depends, status
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
from typing import Dict, Any, Union, List
from pydantic import BaseModel
from google.oauth2 import service_account
from utils.speech_client import get_speech_client

router = APIRouter()

class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Union[Dict[str, Any], List[Dict[str, Any]], None]

def create_response(
    success: bool,
    message: str,
    data: Union[Dict[str, Any], List[Dict[str, Any]], None] = None,
    status_code: int = status.HTTP_200_OK
) -> Dict[str, Any]:
    return {
        "success": success,
        "message": message,
        "data": data
    }

# Initialize Google Cloud Speech client safely
try:
        client = get_speech_client()
except Exception as e:
    client = None
    print(f"Warning: Failed to initialize SpeechClient - {str(e)}")

# Initialize translator
translator = Translator()

@router.post("", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    if not client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=create_response(
                success=False,
                message="Speech-to-text service currently unavailable",
                data=None
            )
        )
    
    try:
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
                    db.commit()
                    return create_response(
                        success=False,
                        message="Voice transcription failed - no results returned",
                        data={"feedback_id": db_feedback.id},
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            except Exception as e:
                db_feedback.processed = False
                db.commit()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=create_response(
                        success=False,
                        message=f"Error processing voice data: {str(e)}",
                        data={"feedback_id": db_feedback.id}
                    )
                )

        db.commit()
        return create_response(
            success=True,
            message="Feedback submitted successfully",
            data=db_feedback,
            status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error submitting feedback: {str(e)}",
                data=None
            )
        )

@router.get("", response_model=StandardResponse)
def get_all_feedback(db: Session = Depends(get_db)):
    try:
        feedback_list = db.query(Feedback).all()
        if not feedback_list:
            return create_response(
                success=True,
                message="No feedback found",
                data=[]
            )
        return create_response(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback_list
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving feedback: {str(e)}",
                data=None
            )
        )

@router.get("/{feedback_id}", response_model=StandardResponse)
def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    try:
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Feedback not found",
                    data=None
                )
            )
        return create_response(
            success=True,
            message="Feedback retrieved successfully",
            data=feedback
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving feedback: {str(e)}",
                data=None
            )
        )

@router.put("/{feedback_id}", response_model=StandardResponse)
def update_feedback(feedback_id: int, feedback_update: FeedbackCreate, db: Session = Depends(get_db)):
    try:
        db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not db_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Feedback not found",
                    data=None
                )
            )
        
        update_data = feedback_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        
        db.commit()
        db.refresh(db_feedback)
        return create_response(
            success=True,
            message="Feedback updated successfully",
            data=db_feedback
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error updating feedback: {str(e)}",
                data=None
            )
        )

@router.delete("/{feedback_id}", response_model=StandardResponse)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    try:
        db_feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if not db_feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Feedback not found",
                    data=None
                )
            )
        
        db.delete(db_feedback)
        db.commit()
        return create_response(
            success=True,
            message="Feedback deleted successfully",
            data={"id": feedback_id}
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error deleting feedback: {str(e)}",
                data=None
            )
        )