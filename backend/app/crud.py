from sqlalchemy.orm import Session
from . import models, schemas

def get_plants(db: Session):
    return db.query(models.Plant).all()

def get_plant(db: Session, plant_id: int):
    return db.query(models.Plant).filter(models.Plant.id == plant_id).first()

def create_plant(db: Session, plant: schemas.PlantSchema):
    db_plant = models.Plant(**plant.dict())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return db_plant

def update_plant(db: Session, db_plant: models.Plant, plant_data: schemas.PlantSchema):
    db_plant.name = plant_data.name
    db_plant.type = plant_data.type
    db_plant.notes = plant_data.notes
    db.commit()
    db.refresh(db_plant)
    return db_plant

def delete_plant(db: Session, db_plant: models.Plant):
    db.delete(db_plant)
    db.commit()
