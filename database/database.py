from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.settings import settings
from databases import Database

# # Create the database engine
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# database = Database( settings.DATABASE_URL)
# Base class for models
Base = declarative_base()

def init_db():
    """Initialize the database by creating all tables."""
    # Import all models here before calling create_all()
    from schemas.user import User
    from schemas.refresh_token import RefreshToken
    
    # Create all tables
    Base.metadata.create_all(bind=engine)

async def get_db():
    """
    Dependency function that yields database sessions.
    Handles session cleanup automatically.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    """
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()
    """
