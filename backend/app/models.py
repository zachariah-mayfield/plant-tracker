from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    water_frequency = Column(String(100), nullable=False)
    sunlight_requirements = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
