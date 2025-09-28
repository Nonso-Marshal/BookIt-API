from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User as DBUser, Role
from schemas.user import UserUpdate, User
from schemas.auth import UserRegister
from passlib.context import CryptContext
from dependency import get_password_hash
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def register_user(db: Session, user_data: UserRegister):
        logger.info(f"Registering user with email: {user_data.email}")
        existing_user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
        if existing_user:
            logger.error(f"User with email {user_data.email} already exists")
            raise ValueError("User with this email already exists")

        logger.info(f"Original password length: {len(user_data.password.encode('utf-8'))} bytes")
        password = user_data.password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        logger.info(f"Truncated password length: {len(password.encode('utf-8'))} bytes")
        hashed_password = get_password_hash(password)

        try:
            role_value = Role[user_data.role.lower()]
        except KeyError:
            logger.error(f"Invalid role: {user_data.role}")
            raise ValueError(f"Invalid role: {user_data.role}. Must be 'user' or 'admin'")

        user = DBUser(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=role_value, 
            created_at=user_data.created_at if hasattr(user_data, 'created_at') else datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"User {user_data.email} registered successfully")
        return user
        
    @staticmethod
    def get_current_user(db: Session, user_id: int) -> User:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User.from_orm(user)

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = db.query(DBUser).filter(DBUser.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        for key, value in user_data.dict(exclude_unset=True).items():
            if key == "password":
                value = get_password_hash(value)
                key = "password_hash"
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        logger.info(f"Updated user ID {user_id}")
        return User.from_orm(user)