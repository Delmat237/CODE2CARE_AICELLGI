from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.feedback import Feedback
from schemas.reminder import Reminder
from models.feedback import FeedbackResponse
from models.reminder import ReminderResponse
from schemas.dashboard import DashboardStatsResponse
from utils.auth import get_current_user, get_current_admin
from datetime import datetime
from typing import Dict, Any, Union, List
from pydantic import BaseModel
from sqlalchemy import func

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

@router.get("/stats", response_model=StandardResponse)
def get_dashboard_stats(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    """
        Retrieve global statistics for feedback and reminders.
        Returns standardized response with success, message, and data fields.
    """
    try:
        # Total feedback
        total_feedback = db.query(Feedback).count()
        # Feedback by rating
        feedback_by_rating_query = db.query(Feedback.overall_experience, func.count(Feedback.overall_experience)).group_by(Feedback.overall_experience).all()
        feedback_by_rating = {rating: count for rating, count in feedback_by_rating_query if rating is not None}
        feedback_by_rating = {i: feedback_by_rating.get(i, 0) for i in range(1, 6)}
        # Reminders by status
        reminders_by_status_query = db.query(Reminder.status, func.count(Reminder.status)).group_by(Reminder.status).all()
        reminders_by_status = {status: count for status, count in reminders_by_status_query if status in ["sent", "failed", "pending"]}
        reminders_by_status = {"sent": reminders_by_status.get("sent", 0), "failed": reminders_by_status.get("failed", 0), "pending": reminders_by_status.get("pending", 0)}
        # Total reminders
        total_reminders = sum(reminders_by_status.values())

        stats = DashboardStatsResponse(
            total_feedback=total_feedback,
            total_reminders=total_reminders,
            feedback_by_rating=feedback_by_rating,
            reminders_by_status=reminders_by_status
        )
        return create_response(
            success=True,
            message="Dashboard statistics retrieved successfully",
            data=stats.dict()
        )
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=create_response(
                    success=False,
                    message=f"Error retrieving dashboard stats: {str(e)}",
                    data=None
                )
            )
    
@router.get("/feedback", response_model=StandardResponse)
def get_feedback_analytics(
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin)
):
    """
    Retrieve analytics for feedback, filtered by date range.
    Returns standardized response with success, message, and data fields.
    """
    try:
        query = db.query(Feedback)
        if start_date:
            query = query.filter(Feedback.feedback_date >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Feedback.feedback_date <= datetime.fromisoformat(end_date))
        
        feedbacks = query.all()
        return create_response(
            success=True,
            message="Feedback analytics retrieved successfully",
            data=feedbacks if feedbacks else []
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_response(
                success=False,
                message=f"Invalid date format: {str(e)}",
                data=None
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving feedback analytics: {str(e)}",
                data=None
            )
        )

@router.get("/reminders", response_model=StandardResponse)
def get_reminder_analytics(
    start_date: str = None,
    end_date: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin)
):
    """
    Retrieve analytics for reminders, filtered by date range and status.
    Returns standardized response with success, message, and data fields.
    """
    try:
        query = db.query(Reminder)
        if start_date:
            query = query.filter(Reminder.scheduled_time >= datetime.fromisoformat(start_date))
        if end_date:
            query = query.filter(Reminder.scheduled_time <= datetime.fromisoformat(end_date))
        if status:
            query = query.filter(Reminder.status == status)
        
        reminders = query.all()
        return create_response(
            success=True,
            message="Reminder analytics retrieved successfully",
            data=reminders if reminders else []
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_response(
                success=False,
                message=f"Invalid date format: {str(e)}",
                data=None
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=create_response(
                success=False,
                message=f"Error retrieving reminder analytics: {str(e)}",
                data=None
            )
        )