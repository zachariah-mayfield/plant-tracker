import yaml
from pathlib import Path
from typing import List
from models import Plant

PLANTS_FILE = Path("data/plants.yaml")

def read_plants() -> List[Plant]:
    if not PLANTS_FILE.exists():
        return []

    with open(PLANTS_FILE, "r") as file:
        data = yaml.safe_load(file) or []
        return [Plant(**item) for item in data]

def write_plants(plants: List[Plant]):
    with open(PLANTS_FILE, "w") as file:
        yaml.safe_dump([plant.dict() for plant in plants], file)

def get_plant_by_name(name: str) -> Plant | None:
    plants = read_plants()
    for plant in plants:
        if plant.name.lower() == name.lower():
            return plant
    return None

def remove_plant_by_name(name: str) -> bool:
    plants = read_plants()
    new_plants = [p for p in plants if p.name.lower() != name.lower()]
    if len(new_plants) == len(plants):
        return False
    write_plants(new_plants)
    return True

def update_plant(name: str, updated: Plant) -> bool:
    plants = read_plants()
    updated_list = []
    found = False
    for plant in plants:
        if plant.name.lower() == name.lower():
            updated_list.append(updated)
            found = True
        else:
            updated_list.append(plant)
    if found:
        write_plants(updated_list)
    return found
