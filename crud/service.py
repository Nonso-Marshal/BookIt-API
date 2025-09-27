from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Service as DBService 
from schemas.service import ServiceCreate, ServiceUpdate, Service as ServiceSchema 
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceService:
    @staticmethod
    def create_service(db: Session, service_data: ServiceCreate) -> ServiceSchema:
        logger.info("Using updated create_service method")
        service_dict = service_data.dict(exclude_unset=True)
        db_service = DBService(
            title=service_dict["title"],
            description=service_dict.get("description"),
            price=service_dict["price"],
            duration_minutes=service_dict["duration_minutes"],
            is_active=service_dict.get("is_active", True)
        )
        try:
            db.add(db_service)
            db.commit()
            db.refresh(db_service)
        except Exception as error:
            db.rollback()
            logger.error(f"Error creating service: {str(error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating service"
            )
        return ServiceSchema.model_validate(db_service)

    @staticmethod
    def get_services(db: Session, q: str = None, price_min: float = None, price_max: float = None, active: bool = None) -> List[ServiceSchema]:
        query = db.query(DBService)
        if q:
            query = query.filter(DBService.title.ilike(f"%{q}%"))
        if price_min is not None:
            query = query.filter(DBService.price >= price_min)
        if price_max is not None:
            query = query.filter(DBService.price <= price_max)
        if active is not None:
            query = query.filter(DBService.is_active == active)
        services = query.all()
        logger.info(f"Retrieved {len(services)} services")
        return [ServiceSchema.model_validate(service) for service in services]

    @staticmethod
    def get_service(db: Session, service_id: int) -> ServiceSchema:
        service = db.query(DBService).filter(DBService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        return ServiceSchema.model_validate(service)

    @staticmethod
    def update_service(db: Session, service_id: int, service_data: ServiceUpdate) -> ServiceSchema:
        service = db.query(DBService).filter(DBService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        for key, value in service_data.dict(exclude_unset=True).items():
            setattr(service, key, value)
        db.commit()
        db.refresh(service)
        logger.info(f"Updated service ID {service_id}")
        return ServiceSchema.model_validate(service)

    @staticmethod
    def delete_service(db: Session, service_id: int) -> None:
        service = db.query(DBService).filter(DBService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
        db.delete(service)
        db.commit()
        logger.info(f"Deleted service ID {service_id}")