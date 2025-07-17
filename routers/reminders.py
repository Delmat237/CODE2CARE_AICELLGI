from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.reminder import Reminder  # SQLAlchemy model
from models.reminder import ReminderCreate, ReminderResponse  # Pydantic models
from utils.twilio_client import send_sms, send_ivr
from utils.email_client import send_email
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Union, List
from pydantic import BaseModel

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

@router.post("", response_model=StandardResponse, status_code=status.HTTP_201_CREATED)
async def schedule_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    try:
        # Timezone conversion
        if reminder.scheduled_time.tzinfo is None:
            reminder.scheduled_time = reminder.scheduled_time.replace(tzinfo=timezone.utc)
        
        # Validate scheduled time is in the future
        if reminder.scheduled_time <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=create_response(
                    success=False,
                    message="Scheduled time must be in the future",
                    data=None
                )
            )

        # Database operations
        db_reminder = Reminder(**reminder.dict(exclude_unset=True))
        db.add(db_reminder)
        db.commit()
        db.refresh(db_reminder)

        # Schedule sending if time is in future
        if datetime.now(timezone.utc) < db_reminder.scheduled_time:
            asyncio.create_task(send_reminder(db_reminder.id, db))

        return create_response(
            success=True,
            message="Reminder scheduled successfully",
            data=db_reminder,
            status_code=status.HTTP_201_CREATED
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error scheduling reminder: {str(e)}",
                data=None
            )
        )

async def send_reminder(reminder_id: int, db: Session):
    try:
        # Get fresh session for background task
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            return

        # Calculate delay
        delay = (reminder.scheduled_time - datetime.now(timezone.utc)).total_seconds()
        if delay > 0:
            await asyncio.sleep(delay)

        # Send reminder
        success = False
        if reminder.channel == "sms" and reminder.phone_number:
            success = await send_sms(reminder.phone_number, reminder.message)
        elif reminder.channel == "ivr" and reminder.phone_number:
            success = await send_ivr(reminder.phone_number, reminder.message)
        elif reminder.channel == "email" and reminder.email:
            success = await send_email(reminder.email, "Reminder", reminder.message)

        # Update status
        reminder.status = "sent" if success else "failed"
        db.commit()
    except Exception as e:
        print(f"Error sending reminder {reminder_id}: {str(e)}")
        if reminder:
            reminder.status = "failed"
            db.commit()
    finally:
        db.close()

@router.get("", response_model=StandardResponse)
def get_all_reminders(db: Session = Depends(get_db)):
    try:
        reminders = db.query(Reminder).all()
        return create_response(
            success=True,
            message="Reminders retrieved successfully",
            data=reminders if reminders else []
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving reminders: {str(e)}",
                data=None
            )
        )

@router.get("/{reminder_id}", response_model=StandardResponse)
def get_reminder_by_id(reminder_id: int, db: Session = Depends(get_db)):
    try:
        reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Reminder not found",
                    data=None
                )
            )
        return create_response(
            success=True,
            message="Reminder retrieved successfully",
            data=reminder
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving reminder: {str(e)}",
                data=None
            )
        )

@router.put("/{reminder_id}", response_model=StandardResponse)
def update_reminder(reminder_id: int, reminder_update: ReminderCreate, db: Session = Depends(get_db)):
    try:
        db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not db_reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Reminder not found",
                    data=None
                )
            )
        
        update_data = reminder_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == "scheduled_time":
                if value.tzinfo is None:
                    value = value.replace(tzinfo=timezone.utc)
                if value <= datetime.now(timezone.utc):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=create_response(
                            success=False,
                            message="Cannot set scheduled time in the past",
                            data=None
                        )
                    )
            setattr(db_reminder, key, value)
        
        db.commit()
        db.refresh(db_reminder)
        
        # Reschedule if needed
        if "scheduled_time" in update_data and datetime.now(timezone.utc) < db_reminder.scheduled_time:
            asyncio.create_task(send_reminder(reminder_id, db))
            
        return create_response(
            success=True,
            message="Reminder updated successfully",
            data=db_reminder
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error updating reminder: {str(e)}",
                data=None
            )
        )

@router.delete("/{reminder_id}", response_model=StandardResponse)
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    try:
        db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
        if not db_reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=create_response(
                    success=False,
                    message="Reminder not found",
                    data=None
                )
            )
        
        db.delete(db_reminder)
        db.commit()
        return create_response(
            success=True,
            message="Reminder deleted successfully",
            data={"id": reminder_id}
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error deleting reminder: {str(e)}",
                data=None
            )
        )