from fastapi import APIRouter, Depends, HTTPException
from models.feedback import FeedbackResponse
from models.reminder import ReminderResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas.feedback import Feedback
from schemas.reminder import Reminder
from schemas.dashboard import DashboardStatsResponse  # Assume this is defined in schemas/dashboard.py
from utils.auth import get_current_user, get_current_admin  # Custom dependencies for admin access
from datetime import datetime

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Retrieve global statistics for feedback and reminders.
    """
    stats = DashboardStatsResponse(
        total_feedback=db.query(Feedback).count(),
        total_reminders=db.query(Reminder).count(),
        feedback_by_rating={
            i: db.query(Feedback).filter(Feedback.overall_experience == i).count()
            for i in range(1, 6)
        },
        reminders_by_status={
            "sent": db.query(Reminder).filter(Reminder.status == "sent").count(),
            "failed": db.query(Reminder).filter(Reminder.status == "failed").count(),
            "pending": db.query(Reminder).filter(Reminder.status == "pending").count()
        }
    )
    return stats

@router.get("/feedback", response_model=list[FeedbackResponse])  # Assume FeedbackResponse is defined
def get_feedback_analytics(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve analytics for feedback, filtered by date range.
    """
    query = db.query(Feedback)
    if start_date:
        query = query.filter(Feedback.feedback_date >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Feedback.feedback_date <= datetime.fromisoformat(end_date))
    
    feedbacks = query.all()
    if not feedbacks:
        raise HTTPException(status_code=404, detail="No feedback data found for the given criteria")
    return feedbacks

@router.get("/reminders", response_model=list[ReminderResponse])  # Assume ReminderResponse is defined
def get_reminder_analytics(
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve analytics for reminders, filtered by date range and status.
    """
    query = db.query(Reminder)
    if start_date:
        query = query.filter(Reminder.scheduled_time >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Reminder.scheduled_time <= datetime.fromisoformat(end_date))
    if status:
        query = query.filter(Reminder.status == status)
    
    reminders = query.all()
    if not reminders:
        raise HTTPException(status_code=404, detail="No reminder data found for the given criteria")
    return reminders