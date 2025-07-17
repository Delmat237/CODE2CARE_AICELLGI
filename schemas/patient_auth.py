from pydantic import BaseModel, EmailStr, validator
import re

class PatientAuthRequest(BaseModel):
    external_id: str
    phone_number: str = None
    email: EmailStr = None

    @validator('external_id')
    def validate_external_id(cls, v):
        if not re.match(r'^P\d{6}$', v):
            raise ValueError('external_id doit être au format "P" suivi de 6 chiffres (ex. P008672)')
        return v

    class Config:
        from_attributes = True  