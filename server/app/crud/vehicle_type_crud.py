from sqlalchemy.orm import Session
from app.models import VehicleType
from app.schemas.vehicle_type_schema import VehicleTypeCreate, VehicleTypeUpdate


def get_vehicle_type_by_name(db: Session, name: str):
    return db.query(VehicleType).filter(VehicleType.name == name).first()


def create_vehicle_type(db: Session, vehicle: VehicleTypeCreate):
    db_vehicle_type = VehicleType(name=vehicle.name, description=vehicle.description)
    db.add(db_vehicle_type)
    db.commit()
    db.refresh(db_vehicle_type)
    return db_vehicle_type


def update_vehicle_type(db: Session, vehicle_id: int, vehicle: VehicleTypeUpdate):
    db_vehicle_type = db.query(VehicleType).filter(VehicleType.id == vehicle_id).first()
    if not db_vehicle_type:
        return None
    setattr(db_vehicle_type, "name", vehicle.name)
    setattr(db_vehicle_type, "description", vehicle.description)

    db.commit()
    db.refresh(db_vehicle_type)
    return db_vehicle_type
