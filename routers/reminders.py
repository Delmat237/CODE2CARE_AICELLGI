from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.reminder import ReminderCreate, ReminderResponse
from schemas.reminder import Reminder
from utils.twilio_client import send_sms, send_ivr
import asyncio
from datetime import datetime

router = APIRouter()

@router.post("/reminders", response_model=ReminderResponse)
async def schedule_reminder(reminder: ReminderCreate, db: Session = Depends(get_db)):
    db_reminder = Reminder(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    # Schedule async task for sending reminder
    if datetime.utcnow() < db_reminder.scheduled_time:
        asyncio.create_task(send_reminder(db_reminder))
    return db_reminder

async def send_reminder(reminder: Reminder):
    await asyncio.sleep((reminder.scheduled_time - datetime.utcnow()).total_seconds())
    success = await send_sms(reminder.phone_number, reminder.message) or await send_ivr(reminder.phone_number, reminder.message)
    reminder.status = "sent" if success else "failed"
    with SessionLocal() as db:
        db.merge(reminder)
        db.commit()