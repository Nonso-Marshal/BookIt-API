from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import status, HTTPException
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    logger.error("DATABASE_URL environment variable not set")
    raise ValueError("DATABASE_URL environment variable not set")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://"), echo=True)
except Exception as error:
    logger.error(f"Failed to connect to database: {str(error)}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to connect to database: {str(error)}"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()