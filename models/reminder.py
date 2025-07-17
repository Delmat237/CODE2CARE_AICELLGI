from pydantic import BaseModel, Field
from datetime import datetime

class ReminderBase(BaseModel):
    patient_id: str = Field(..., example="PAT123")
    message: str = Field(..., example="Rappel: RDV à 10h")
    language: str = Field(..., example="french", enum=["english", "french", "douala", "bassa", "ewondo"])
    scheduled_time: datetime = Field(..., example="2025-07-14T10:00:00")
    phone_number: str = Field(..., example="+237XXXXXXXX")
    email: str = Field(None, example="azangueleonel9@gmail.com")
    channel: str = Field(..., example="sms", enum=["sms", "ivr", "email"])

class ReminderCreate(ReminderBase):
    pass

class ReminderResponse(ReminderBase):
    id: int
    status: str = Field(..., example="pending")
    created_at: datetime = Field(..., example="2025-07-14T09:00:00")
    channel: str = Field(..., example="sms", enum=["sms", "ivr", "email"])  

    class Config:
        orm_mode = True