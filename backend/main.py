from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routers import plants
from app.security import setup_security_middleware
import logging

# Load DB connection from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/plantdb")

# Set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Plant model
class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

# Create table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Pydantic schema for input/output
class PlantSchema(BaseModel):
    name: str
    type: str = ""
    notes: str = ""

class PlantOutSchema(PlantSchema):
    id: int

    class Config:
        orm_mode = True

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Plant Tracker API",
    description="API for tracking plants and their care",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Setup security middleware
setup_security_middleware(app)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"Home Page: This is the Plant Tracker API. Use /docs for Swagger UI."}

# Health check
@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return {"db_alive": result.scalar() == 1}
    except Exception as e:
        return {"error": str(e)}

# Get all plants
@app.get("/plants", response_model=List[PlantOutSchema])
def read_plants(db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return plants

# Get plant by ID
@app.get("/plants/{id}", response_model=PlantOutSchema)
def read_plant(id: int, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == id).first()
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plant

# Create a new plant
@app.post("/plants", response_model=PlantOutSchema)
def create_plant(plant: PlantSchema, db: Session = Depends(get_db)):
    db_plant = Plant(**plant.dict())
    try:
        db.add(db_plant)
        db.commit()
        db.refresh(db_plant)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Plant with that name might already exist.")
    return db_plant

# Update an existing plant
@app.put("/plants/{id}", response_model=PlantOutSchema)
def update_plant(id: int, plant: PlantSchema, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    db_plant.name = plant.name
    db_plant.type = plant.type
    db_plant.notes = plant.notes

    db.commit()
    db.refresh(db_plant)
    return db_plant

# Delete a plant
@app.delete("/plants/{id}")
def delete_plant(id: int, db: Session = Depends(get_db)):
    db_plant = db.query(Plant).filter(Plant.id == id).first()
    if db_plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    db.delete(db_plant)
    db.commit()
    return {"message": f"Plant with id {id} has been deleted."}

# Include routers
app.include_router(plants.router, prefix="/api/v1")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}
