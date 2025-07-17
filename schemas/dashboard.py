from pydantic import BaseModel
from typing import Dict

class DashboardStatsResponse(BaseModel):
    total_feedback: int
    total_reminders: int
    feedback_by_rating: Dict[int, int] 
    reminders_by_status: Dict[str, int]  

    class Config:
        orm_mode = True