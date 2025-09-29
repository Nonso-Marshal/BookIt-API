from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dependency import verify_password, create_access_token, create_refresh_token, get_current_user
from crud.user import UserService
from schemas.auth import UserRegister, UserLogin, Token
from models import User as DBUser
from schemas.user import UserResponse
from database import get_db
import logging
import os
from jose import jwt, JWTError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = UserService.register_user(db, user_data)
        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role.value})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except ValueError as e:
        logger.error(f"Registration failed for {user_data.email}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during registration for {user_data.email}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

@auth_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    logger.debug(f"Login attempt for email: {user_data.email}")
    logger.debug(f"Received payload: {user_data.dict()}")
    user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        logger.error(f"Login failed for {user_data.email}: Invalid credentials")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
    refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role.value})
    logger.info(f"Login successful for {user_data.email}")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@auth_router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="auth/login")), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        user = db.query(DBUser).filter(DBUser.id == int(user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
        refresh_token = create_refresh_token({"sub": str(user.id), "role": user.role.value})
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    return None