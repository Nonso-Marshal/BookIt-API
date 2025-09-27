from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Booking as DBBooking, BookingStatus, Service 
from schemas.booking import BookingCreate, BookingUpdate, Booking as BookingSchema 
from datetime import datetime, timedelta
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BookingService:
    @staticmethod
    def create_booking(db: Session, booking_data: BookingCreate, user_id: int) -> BookingSchema:
        service = db.query(Service).filter(Service.id == booking_data.service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        if not service.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Service is not active")
        
        end_time = booking_data.start_time + timedelta(minutes=service.duration_minutes)

        overlap = db.query(DBBooking).filter(
            DBBooking.service_id == booking_data.service_id,
            DBBooking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            DBBooking.start_time < end_time,
            DBBooking.end_time > booking_data.start_time
        ).first()
        if overlap:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Booking conflicts with existing booking")
        
        booking = DBBooking(
            user_id=user_id,
            service_id=booking_data.service_id,
            start_time=booking_data.start_time,
            end_time=end_time,
            status=BookingStatus.PENDING,
            created_at=datetime.utcnow()
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        logger.info(f"Created booking ID {booking.id}")
        return BookingSchema.model_validate(booking)

    @staticmethod
    def get_bookings(db: Session, user_id: int, role: str, status: str = None, from_date: datetime = None, to_date: datetime = None) -> List[BookingSchema]:
        query = db.query(DBBooking)
        if role == "user":
            query = query.filter(DBBooking.user_id == user_id)
        if status:
            query = query.filter(DBBooking.status == BookingStatus[status.upper()])
        if from_date:
            query = query.filter(DBBooking.start_time >= from_date)
        if to_date:
            query = query.filter(DBBooking.start_time <= to_date)
        bookings = query.all()
        logger.info(f"Retrieved {len(bookings)} bookings")
        return [BookingSchema.model_validate(booking) for booking in bookings]

    @staticmethod
    def get_booking(db: Session, booking_id: int, user_id: int, role: str) -> BookingSchema:
        booking = db.query(DBBooking).filter(DBBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if role == "user" and booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this booking")
        return BookingSchema.model_validate(booking)

    @staticmethod
    def update_booking(db: Session, booking_id: int, booking_data: BookingUpdate, user_id: int, role: str) -> BookingSchema:
        booking = db.query(DBBooking).filter(DBBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if role == "user" and booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this booking")
        if role == "user" and booking.status not in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update booking in this status")
        if role == "user" and booking_data.status and booking_data.status not in ["cancelled"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users can only cancel bookings")
        
        if booking_data.start_time:
            service = db.query(Service).filter(Service.id == booking.service_id).first()
            new_end_time = booking_data.start_time + timedelta(minutes=service.duration_minutes)
            overlap = db.query(DBBooking).filter(
                DBBooking.service_id == booking.service_id,
                DBBooking.id != booking_id,
                DBBooking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
                and_(
                    DBBooking.start_time < new_end_time,
                    DBBooking.end_time > booking_data.start_time
                )
            ).first()
            if overlap:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="New time conflicts with existing booking")
            booking.start_time = booking_data.start_time
            booking.end_time = new_end_time
        
        if booking_data.status:
            booking.status = BookingStatus[booking_data.status.upper()]
        
        db.commit()
        db.refresh(booking)
        logger.info(f"Updated booking ID {booking_id}")
        return BookingSchema.model_validate(booking)

    @staticmethod
    def delete_booking(db: Session, booking_id: int, user_id: int, role: str) -> None:
        booking = db.query(DBBooking).filter(DBBooking.id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
        if role == "user" and booking.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this booking")
        if role == "user" and booking.start_time <= datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete past or ongoing booking")
        db.delete(booking)
        db.commit()
        logger.info(f"Deleted booking ID {booking_id}")