from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ServiceBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    duration_minutes: int
    is_active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    duration_minutes: Optional[int] = None
    is_active: Optional[bool] = None

class Service(ServiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True