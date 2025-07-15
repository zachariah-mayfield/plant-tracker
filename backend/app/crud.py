from sqlalchemy.orm import Session
from . import models, schemas

def get_plants(db: Session):
    return db.query(models.Plant).all()

def get_plant(db: Session, plant_id: int):
    return db.query(models.Plant).filter(models.Plant.id == plant_id).first()

def create_plant(db: Session, plant: schemas.PlantCreate):
    db_plant = models.Plant(**plant.model_dump())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def update_plant(db: Session, db_plant: models.Plant, plant_data: schemas.PlantUpdate):
    update_data = plant_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_plant, field, value)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def delete_plant(db: Session, db_plant: models.Plant):
    db.delete(db_plant)
    db.commit()
