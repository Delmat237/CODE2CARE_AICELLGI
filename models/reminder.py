from pydantic import BaseModel, Field,validator
from datetime import datetime
import re

class ReminderBase(BaseModel):
    patient_id: str = Field(..., example="P008672")
    message: str = Field(..., example="Rappel: RDV à 10h")
    language: str = Field(..., example="french", enum=["english", "french", "douala", "bassa", "ewondo"])
    scheduled_time: datetime = Field(..., example="2025-07-14T10:00:00Z")
    phone_number: str = Field(..., example="+237XXXXXXXX")
    email: str = Field(None, example="azangueleonel9@gmail.com")
    channel: str = Field(..., example="sms", enum=["sms", "ivr", "email"])

class ReminderCreate(ReminderBase):
    @validator('patient_id')
    def validate_id(cls, v):
        if not re.match(r'^P\d{6}$', v):
            raise ValueError('id doit être au format "P" suivi de 6 chiffres (ex. P008672)')
        return v
    pass

class ReminderResponse(ReminderBase):
    id: int
    status: str = Field(..., example="pending")
    created_at: datetime = Field(..., example="2025-07-14T09:00:00Z")
    channel: str = Field(..., example="sms", enum=["sms", "ivr", "email"])  
    status:str | None = None

    class Config:
        orm_mode = True