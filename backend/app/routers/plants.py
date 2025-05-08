from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()

@router.get("/plants", response_model=list[schemas.PlantOut])
def read_plants(db: Session = Depends(get_db)):
    return crud.get_plants(db)

@router.get("/plants/{id}", response_model=schemas.PlantOut)
def read_plant(id: int, db: Session = Depends(get_db)):
    plant = crud.get_plant(db, id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

@router.post("/plants", response_model=schemas.PlantOut)
def create_plant(plant: schemas.PlantCreate, db: Session = Depends(get_db)):
    return crud.create_plant(db, plant)

@router.put("/plants/{id}", response_model=schemas.PlantOut)
def update_plant(id: int, plant: schemas.PlantUpdate, db: Session = Depends(get_db)):
    db_plant = crud.get_plant(db, id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return crud.update_plant(db, db_plant, plant)

@router.delete("/plants/{id}")
def delete_plant(id: int, db: Session = Depends(get_db)):
    db_plant = crud.get_plant(db, id)
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    crud.delete_plant(db, db_plant)
    return {"message": f"Plant with id {id} has been deleted."}
