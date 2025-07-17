from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/feedback_db"
    
    # Twilio Configuration
    TWILIO_ACCOUNT_SID: str = ""  # Fixed typo in variable name (ACCOUNT instead of ACCOUNT)
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Authentication Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_SECRET_KEY: str = "your-refresh-secret-key-here"  # Consistent naming
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Email Configuration
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""  # More standard than SMTP_PASS
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USE_TLS: bool = True  # Added for explicit TLS configuration
    
    # Application Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS Configuration (Recommended)
    CORS_ORIGINS: list[str] = ["*"]  # Restrict in production!
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Optional: Google Cloud or Logging Settings
    GOOGLE_APPLICATION_CREDENTIALS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars rather than raising errors

settings = Settings()