"""
Pydantic models for request/response validation
SQLAlchemy models for database entities
"""

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from typing import List, Optional, Dict
from datetime import datetime

Base = declarative_base()

# Pydantic models for API
class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="Message de l'utilisateur")
    language: str = Field(default="fr", description="Langue de la conversation")
    session_id: str = Field(..., description="ID de session pour le suivi")
    user_context: Optional[Dict] = Field(default=None, description="Contexte utilisateur (âge, localisation, etc.)")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Réponse du chatbot")
    session_id: str = Field(..., description="ID de session")
    language: str = Field(..., description="Langue de la réponse")
    confidence: float = Field(..., description="Score de confiance de la réponse")
    suggestions: List[str] = Field(default=[], description="Suggestions de questions de suivi")

class ConversationHistory(BaseModel):
    """Model for conversation history"""
    id: int
    user_id: str
    session_id: str
    message: str
    response: str
    language: str
    timestamp: datetime
    evaluation_score: float

    class Config:
        orm_mode = True

# SQLAlchemy models for database
class Conversation(Base):
    """Database model for storing conversations"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    session_id = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    language = Column(String, default="fr")
    timestamp = Column(DateTime, default=func.now())
    evaluation_score = Column(Float, default=0.8)
    is_encrypted = Column(Boolean, default=False)

class User(Base):
    """Database model for users"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    last_active = Column(DateTime, default=func.now())
    preferred_language = Column(String, default="fr")
    total_conversations = Column(Integer, default=0)

class MedicalKnowledge(Base):
    """Database model for medical knowledge base"""
    __tablename__ = "medical_knowledge"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # diagnostic, medication, care_instruction
    condition = Column(String, index=True)
    symptoms = Column(Text)
    treatment = Column(Text)
    cultural_context = Column(Text)  # Adaptations culturelles
    language = Column(String, default="fr")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())