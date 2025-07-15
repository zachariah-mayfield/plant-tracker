from fastapi import FastAPI
from .routers import plants, health
from .database import Base, engine
import os

# Only create tables if not in test environment
if not os.environ.get("TESTING"):
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(health.router)
app.include_router(plants.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Plant Tracker API"}
