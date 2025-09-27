from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from crud.user import UserService
from schemas.user import User, UserUpdate
from dependency import get_current_user, role_required
from database import get_db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

user_router = APIRouter(prefix="/user", tags=["Users"])

@user_router.get("/", response_model=User, status_code=status.HTTP_200_OK)
def get_user(current_user: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current_user
    return UserService.get_current_user(db, user.id)

@user_router.patch("/", response_model=User, status_code=status.HTTP_200_OK)
def update_me(user_data: UserUpdate, current_user: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    user, _ = current_user
    return UserService.update_user(db, user.id, user_data)