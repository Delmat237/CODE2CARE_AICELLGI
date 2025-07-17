from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.reminder import Reminder  # SQLAlchemy model
from models.reminder import ReminderCreate, ReminderResponse  # Pydantic models
from utils.twilio_client import send_sms, send_ivr
from utils.email_client import send_email
import asyncio
from datetime import datetime
from utils.auth import get_current_user

router = APIRouter()

@router.post("", response_model=ReminderResponse)
async def schedule_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    db_reminder = Reminder(**reminder.dict(exclude_unset=True))
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    # Schedule async task for sending reminder if scheduled time is in the future
    if datetime.utcnow() < db_reminder.scheduled_time:
        asyncio.create_task(send_reminder(db_reminder.id, db))
    return db_reminder

async def send_reminder(reminder_id: int, db: Session):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        return  # Reminder might have been deleted

    await asyncio.sleep((reminder.scheduled_time - datetime.utcnow()).total_seconds())
    success = False
    if reminder.channel == "sms" and reminder.phone_number:
        success = await send_sms(reminder.phone_number, reminder.message)
    elif reminder.channel == "ivr" and reminder.phone_number:
        success = await send_ivr(reminder.phone_number, reminder.message)
    elif reminder.channel == "email" and reminder.email:
        success = await send_email(reminder.email, "Reminder", reminder.message)

    reminder.status = "sent" if success else "failed"
    db.commit()  # Use the passed session to update

@router.get("", response_model=list[ReminderResponse])
def get_all_reminders(db: Session = Depends(get_db)):
    reminders = db.query(Reminder).all()
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminders found")
    return reminders

@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder_by_id(reminder_id: int, db: Session = Depends(get_db)):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder

@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(reminder_id: int, reminder_update: ReminderCreate, db: Session = Depends(get_db)):
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    
    update_data = reminder_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "scheduled_time" and datetime.utcnow() > value:
            raise HTTPException(status_code=400, detail="Cannot set scheduled time in the past")
        setattr(db_reminder, key, value)
    
    db.commit()
    db.refresh(db_reminder)
    # Reschedule if scheduled_time changed and is in the future
    if "scheduled_time" in update_data and datetime.utcnow() < db_reminder.scheduled_time:
        asyncio.create_task(send_reminder(reminder_id, db))
    return db_reminder

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int, db: Session = Depends(get_db)):
    db_reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    db.delete(db_reminder)
    db.commit()
    return {"message": "Reminder deleted successfully"}