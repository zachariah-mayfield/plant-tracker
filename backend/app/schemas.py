from pydantic import BaseModel, Field
from typing import Optional

class PlantBase(BaseModel):
    name: str = Field(..., example="Tomato")
    type: str = Field(..., example="Vegetable")
    water_frequency: str = Field(..., example="Every 2 days")
    sunlight_requirements: str = Field(..., example="Full Sun")
    notes: Optional[str] = Field(None, example="Started from seed")

class PlantCreate(PlantBase):
    pass

class PlantUpdate(PlantBase):
    pass

class PlantOut(PlantBase):
    id: int

    class Config:
        from_attributes = True  # required for Pydantic v2
