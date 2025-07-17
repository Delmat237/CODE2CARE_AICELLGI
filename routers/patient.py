from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.patient import PatientCreate, PatientResponse
from schemas.patient import Patient  # SQLAlchemy model
from utils.auth import get_current_user
from sqlalchemy.exc import IntegrityError
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
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    try:
        db_patient = Patient(**patient.dict(exclude_unset=True))
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return create_response(
            success=True,
            message="Patient created successfully",
            data=db_patient,
            status_code=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        db.rollback()
        if "unique constraint" in str(e.orig) and "ix_patients_email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=create_response(
                    success=False,
                    message="Email already exists. Please use a different email.",
                    data=None
                )
            )
        elif "unique constraint" in str(e.orig) and "ix_patients_external_id" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=create_response(
                    success=False,
                    message="External ID already exists. Please use a different ID.",
                    data=None
                )
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_response(
                success=False,
                message=f"An error occurred: {str(e.orig)}",
                data=None
            )
        )

@router.get("", response_model=StandardResponse)
def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()
    if not patients:
        return create_response(
            success=True,
            message="No patients found",
            data=[]
        )
    return create_response(
        success=True,
        message="Patients retrieved successfully",
        data=patients
    )

@router.get("/{patient_id}", response_model=StandardResponse)
def get_patient_by_id(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_response(
                success=False,
                message="Patient not found",
                data=None
            )
        )
    return create_response(
        success=True,
        message="Patient retrieved successfully",
        data=patient
    )

@router.put("/{patient_id}", response_model=StandardResponse)
def update_patient(patient_id: int, patient_update: PatientCreate, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_response(
                success=False,
                message="Patient not found",
                data=None
            )
        )
    
    update_data = patient_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)
    
    try:
        db.commit()
        db.refresh(db_patient)
        return create_response(
            success=True,
            message="Patient updated successfully",
            data=db_patient
        )
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=create_response(
                success=False,
                message=f"Database error: {str(e.orig)}",
                data=None
            )
        )

@router.delete("/{patient_id}", response_model=StandardResponse)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_response(
                success=False,
                message="Patient not found",
                data=None
            )
        )
    
    db.delete(db_patient)
    db.commit()
    return create_response(
        success=True,
        message="Patient deleted successfully",
        data={"id": patient_id}
    )