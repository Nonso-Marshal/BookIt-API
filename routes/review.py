# routes/review.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.review import ReviewCreate, ReviewUpdate, Review
from crud.review import ReviewService
from database import get_db
from dependency import get_current_user
from models import User as DBUser 
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

review_router = APIRouter(prefix="/reviews", tags=["Reviews"])

@review_router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: Tuple[DBUser, str] = Depends(get_current_user)):
    user, _ = current_user  
    return ReviewService.create_review(db, review, user.id)

@review_router.get("/services/{service_id}/reviews", response_model=List[Review], status_code=status.HTTP_200_OK)
def get_service_reviews(service_id: int, db: Session = Depends(get_db)):
    return ReviewService.get_reviews_by_service(db, service_id)

@review_router.patch("/{review_id}", response_model=Review, status_code=status.HTTP_200_OK)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db), current_user: Tuple[DBUser, str] = Depends(get_current_user)):
    user, _ = current_user 
    return ReviewService.update_review(db, review_id, review_update, user.id)

@review_router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: Tuple[DBUser, str] = Depends(get_current_user)):
    user, role = current_user 
    return ReviewService.delete_review(db, review_id, user.id, role == "ADMIN")