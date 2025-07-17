from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from database import get_db
from utils.auth import authenticate_user, create_access_token, get_current_user, create_refresh_token, validate_refresh_token
from pydantic import BaseModel
from datetime import timedelta
from config.settings import settings
from schemas.user import User, pwd_context  # For database model and hashing
from schemas.user import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from schemas.refresh_token import RefreshToken  # Import the RefreshToken model
from utils.twilio_client import send_sms
from utils.email_client import send_email
from fastapi import status
from schemas.patient_auth import PatientAuthRequest
from schemas.patient import Patient

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
        db=db  
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=UserResponse)
async def register(
    register_request: RegisterRequest, 
    db: Session = Depends(get_db)
):
    # Validation checks
    if db.query(User).filter(User.username == register_request.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if db.query(User).filter(User.email == register_request.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    if register_request.phone_number and db.query(User).filter(
        User.phone_number == register_request.phone_number
    ).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")

    # Create user
    hashed_password = pwd_context.hash(register_request.password)
    db_user = User(
        username=register_request.username,
        email=register_request.email,
        hashed_password=hashed_password,
        phone_number=register_request.phone_number,
        role=register_request.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send welcome message via Twilio (SMS)
    if db_user.phone_number:
        sms_message = f"Bienvenue {db_user.username} ! Votre inscription à l'Hôpital Général de Douala est confirmée. Merci !"
        try:
            await send_sms(db_user.phone_number, sms_message)  # Attend la coroutine
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")  # Log error, continue

    # Send welcome email
    email_subject = "Bienvenue à l'Hôpital Général de Douala"
    email_body = f"""
    Cher(e) {db_user.username},

    Bienvenue dans notre système ! Votre inscription est confirmée avec l'email {db_user.email}. Nous sommes ravis de vous compter parmi nous.

    
    Cordialement,
    L'équipe de l'Hôpital Général de Douala
    """
    #Votre code de connexion est {db_user.external_id}.
    try:
        await send_email(db_user.email, email_subject, email_body)  # Attend la coroutine
    except Exception as e:
        print(f"Failed to send email: {str(e)}")  # Log error, continue

    return {
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    username = validate_refresh_token(refresh_token)
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user or inactive account"
        )
    
    # Invalidate old refresh token
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).update({"is_revoked": True})
    
    # Create new tokens
    new_access_token = create_access_token(data={"sub": user.username, "role": user.role})
    new_refresh_token = create_refresh_token(data={"sub": user.username}, db=db)
    
    db.commit()
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(
    refresh_token: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.username == current_user["username"]
    ).first()
    
    if db_token:
        db_token.is_revoked = True
        db.commit()
    
    return {"message": "Successfully logged out"}

@router.post("/patient", response_model=dict)
async def authenticate_patient(
    auth_data: PatientAuthRequest,
    db: Session = Depends(get_db)
):
    # Vérifier que soit phone_number soit email est fourni, mais pas les deux
    if not auth_data.phone_number and not auth_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un numéro de téléphone ou un email est requis."
        )
    if auth_data.phone_number and auth_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fournissez soit un numéro de téléphone, soit un email, pas les deux."
        )

    # Rechercher le patient dans la base de données
    query = db.query(Patient).filter(Patient.external_id == auth_data.external_id)
    if auth_data.phone_number:
        patient = query.filter(Patient.phone_number == auth_data.phone_number).first()
    elif auth_data.email:
        patient = query.filter(Patient.email == auth_data.email).first()
    else:
        patient = None

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides."
        )

    # Générer un token JWT
    access_token = create_access_token(
        data={"sub": patient.external_id, "type": "patient"},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "patient_id": patient.external_id
    }

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user