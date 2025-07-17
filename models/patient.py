from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

class PatientBase(BaseModel):
    external_id: str
    name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    condition: Optional[str] = None

class PatientCreate(PatientBase):
    @validator('external_id')
    def validate_id(cls, v):
        if not re.match(r'^P\d{6}$', v):
            raise ValueError('id doit être au format "P" suivi de 6 chiffres (ex. P008672)')
        return v

class PatientResponse(PatientBase):
    id: int  # Correspond à Column(Integer)
    registration_date: datetime  # Correspond à Column(DateTime)

    class Config:
        orm_mode = True

    # Méthode optionnelle pour formater registration_date en chaîne si nécessaire
    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data['registration_date'] = data['registration_date'].isoformat() if data['registration_date'] else None
        return data