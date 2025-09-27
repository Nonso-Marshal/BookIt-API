from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from crud.booking import BookingService
from schemas.booking import BookingCreate, BookingUpdate, Booking
from dependency import get_current_user, role_required
from database import get_db
from typing import List
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

booking_router = APIRouter(prefix="/bookings", tags=["Bookings"])

@booking_router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(role_required(["user"]))
):
    user, _ = current_user
    return BookingService.create_booking(db, booking, user.id)

@booking_router.get("/", response_model=List[Booking], status_code=status.HTTP_200_OK)
def get_bookings(
    status: str = None,
    from_date: datetime = None,
    to_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    user, role = current_user
    return BookingService.get_bookings(db, user.id, role, status, from_date, to_date)

@booking_router.get("/{id}", response_model=Booking, status_code=status.HTTP_200_OK)
def get_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    user, role = current_user
    return BookingService.get_booking(db, id, user.id, role)

@booking_router.patch("/{id}", response_model=Booking, status_code=status.HTTP_200_OK)
def update_booking(
    id: int,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    user, role = current_user
    return BookingService.update_booking(db, id, booking, user.id, role)

@booking_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(get_current_user)
):
    user, role = current_user
    BookingService.delete_booking(db, id, user.id, role)