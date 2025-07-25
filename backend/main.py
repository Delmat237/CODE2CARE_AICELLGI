"""
Main FastAPI application for the African Medical Chatbot
Handles API endpoints, authentication, and conversation management
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional

from .database import get_db, init_db
from .models import ChatRequest, ChatResponse, ConversationHistory
from .chatbot import MedicalChatbot
from .auth import create_access_token, verify_token
from .privacy import encrypt_message, decrypt_message
from .evaluation import evaluate_response
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title="African Medical Chatbot API",
    description="Chatbot médical conversationnel adapté au contexte africain",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize chatbot
chatbot = MedicalChatbot()

@app.on_event("startup")
async def startup_event():
    """Initialize database and load models on startup"""
    init_db()
    await chatbot.load_model()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return access token
    For demo purposes, accepts any username/password
    """
    # In production, implement proper user authentication
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        user_id = verify_token(token)

        # Ajoute ces logs :
        print("🧾 Message reçu :", request.message)
        print("📍 Langue :", request.language)
        print("🧠 Contexte utilisateur :", request.user_context)

        history = chatbot.get_conversation_history(db, user_id, request.session_id)

        response = await chatbot.generate_response(
            message=request.message,
            language=request.language,
            history=history,
            user_context=request.user_context
        )
        
        # Evaluate response quality
        evaluation = evaluate_response(request.message, response)
        
        # Save conversation to database (encrypted)
        encrypted_message = encrypt_message(request.message) if settings.ENCRYPT_CONVERSATIONS else request.message
        encrypted_response = encrypt_message(response) if settings.ENCRYPT_CONVERSATIONS else response
        
        chatbot.save_conversation(
            db=db,
            user_id=user_id,
            session_id=request.session_id,
            message=encrypted_message,
            response=encrypted_response,
            language=request.language,
            evaluation_score=evaluation.get('score', 0.8)
        )
        
        return ChatResponse(
            response=response,
            session_id=request.session_id,
            language=request.language,
            confidence=evaluation.get('confidence', 0.8),
            suggestions=evaluation.get('suggestions', [])
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du traitement de votre message: {str(e)}"
        )

@app.get("/history/{session_id}")
async def get_conversation_history(
    session_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Retrieve conversation history for a specific session
    """
    user_id = verify_token(token)
    history = chatbot.get_conversation_history(db, user_id, session_id)
    
    # Decrypt messages if encryption is enabled
    if settings.ENCRYPT_CONVERSATIONS:
        for item in history:
            item.message = decrypt_message(item.message)
            item.response = decrypt_message(item.response)
    
    return history

@app.delete("/history/{session_id}")
async def delete_conversation_history(
    session_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Delete conversation history for privacy
    """
    user_id = verify_token(token)
    chatbot.delete_conversation_history(db, user_id, session_id)
    return {"message": "Historique de conversation supprimé"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model_loaded": chatbot.model_loaded}

@app.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "fr", "name": "Français"},
            {"code": "en", "name": "English"},
            {"code": "wolof", "name": "Wolof"},
            {"code": "hausa", "name": "Hausa"},
            {"code": "swahili", "name": "Swahili"}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )