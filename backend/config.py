"""
Configuration management using environment variables
"""

import os
from dotenv import load_dotenv,find_dotenv
# config.py
from pydantic import BaseSettings



env_path = find_dotenv()
print("📄 .env détecté :", env_path)
load_dotenv(env_path)
print("DATABASE_URL:", os.getenv("DATABASE_URL"))
print("HF_API_TOKEN:", os.getenv("HF_API_TOKEN"))
class Settings:
    """Application settings"""

    MODEL_NAME: str = "C:\\Users\\JUNIOR\\Desktop\\personnel\\aicell\\CODE2CARE_AICELLGI\\tinyllama-lora-checkpoint"  # <-- chemin vers dossier contenant config.json + tokenizer
    LOCAL_WEIGHTS_PATH: str = "C:\\Users\\JUNIOR\\Desktop\\personnel\\aicell\\CODE2CARE_AICELLGI\\tinyllama-lora-checkpoint\\model.pt"
    
    MAX_TOKENS: int = 256
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    ENCRYPT_CONVERSATIONS: bool = False
    # Hugging Face Configuration
    # HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")
    # MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medical_chatbot.db")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Security Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Language Configuration
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "fr")
    SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "fr,en,wolof,hausa,swahili").split(",")
    
    # Privacy Configuration
    ENCRYPT_CONVERSATIONS = os.getenv("ENCRYPT_CONVERSATIONS", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "50"))
    
    # Model Configuration
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "512"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    TOP_P = float(os.getenv("TOP_P", "0.9"))

settings = Settings()