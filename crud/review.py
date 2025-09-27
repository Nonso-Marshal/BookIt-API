from sqlalchemy.orm import Session
from models import Review as DBReview, Booking, BookingStatus
from schemas.review import ReviewCreate, ReviewUpdate, Review as ReviewSchema
from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def create_review(db: Session, review: ReviewCreate, user_id: int):
        booking = db.query(Booking).filter(Booking.id == review.booking_id).first()
        if not booking:
            logger.error(f"Booking ID {review.booking_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if booking.user_id != user_id:
            logger.error(f"User ID {user_id} not authorized for booking ID {review.booking_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        if booking.status != BookingStatus.COMPLETED:
            logger.error(f"Booking ID {review.booking_id} is not completed")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking must be completed")
        existing_review = db.query(DBReview).filter(DBReview.booking_id == review.booking_id).first()
        if existing_review:
            logger.error(f"Review already exists for booking ID {review.booking_id}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review already exists")
        db_review = DBReview(
            booking_id=review.booking_id,
            user_id=booking.user_id,
            service_id=booking.service_id,
            rating=review.rating,
            comment=review.comment
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        logger.info(f"Created review ID {db_review.id}")
        return ReviewSchema.model_validate(db_review)

    @staticmethod
    def update_review(db: Session, review_id: int, review_update: ReviewUpdate, user_id: int):
        db_review = db.query(DBReview).filter(DBReview.id == review_id).first()
        if not db_review:
            logger.error(f"Review ID {review_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        if db_review.user_id != user_id:
            logger.error(f"User ID {user_id} not authorized for review ID {review_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        for key, value in review_update.dict(exclude_unset=True).items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
        logger.info(f"Updated review ID {review_id}")
        return ReviewSchema.model_validate(db_review)

    @staticmethod
    def delete_review(db: Session, review_id: int, user_id: int, is_admin: bool):
        db_review = db.query(DBReview).filter(DBReview.id == review_id).first()
        if not db_review:
            logger.error(f"Review ID {review_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        if db_review.user_id != user_id and not is_admin:
            logger.error(f"User ID {user_id} not authorized to delete review ID {review_id}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        db.delete(db_review)
        db.commit()
        logger.info(f"Deleted review ID {review_id}")
        return {"detail": "Review deleted"}

    @staticmethod
    def get_reviews_by_service(db: Session, service_id: int):
        reviews = db.query(DBReview).filter(DBReview.service_id == service_id).all()
        logger.info(f"Retrieved {len(reviews)} reviews for service ID {service_id}")
        return [ReviewSchema.model_validate(review) for review in reviews]