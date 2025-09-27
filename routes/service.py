from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from crud.service import ServiceService
from schemas.service import ServiceCreate, ServiceUpdate, Service
from dependency import role_required
from database import get_db
from typing import List
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

service_router = APIRouter(prefix="/services", tags=["Services"])

@service_router.get("/", response_model=List[Service])
def get_services(
    q: str = None,
    price_min: float = None,
    price_max: float = None,
    active: bool = None,
    db: Session = Depends(get_db)
):
    return ServiceService.get_services(db, q, price_min, price_max, active)

@service_router.get("/{id}", response_model=Service, status_code=status.HTTP_200_OK)
def get_service(id: int, db: Session = Depends(get_db)):
    return ServiceService.get_service(db, id)

@service_router.post("/", response_model=Service, status_code=status.HTTP_201_CREATED)
def create_service(
    service: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(role_required(["ADMIN"]))
):
    logger.debug(f"Received service payload: {service.dict()}")
    return ServiceService.create_service(db, service)

@service_router.patch("/{id}", response_model=Service, status_code=status.HTTP_200_OK)
def update_service(
    id: int,
    service: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(role_required(["ADMIN"]))
):
    return ServiceService.update_service(db, id, service)

@service_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    id: int,
    db: Session = Depends(get_db),
    current_user: tuple = Depends(role_required(["ADMIN"]))
):
    ServiceService.delete_service(db, id)