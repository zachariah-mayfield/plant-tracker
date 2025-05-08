from fastapi import FastAPI
from .routers import plants, health
from .database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(health.router)
app.include_router(plants.router)
