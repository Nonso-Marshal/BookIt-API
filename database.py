from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import status, HTTPException
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    engine = None 


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    if engine is None:
        raise HTTPException(status_code=500, detail="Database connection not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()