from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    service_id: int
    start_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    status: Optional[str] = None

class Booking(BookingBase):
    id: int
    user_id: int
    end_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True