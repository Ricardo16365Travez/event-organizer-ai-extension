from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Space
import random
from app.schemas import SpaceCreate, SpaceResponse  

router = APIRouter()

# Crear un espacio
@router.post("/spaces", response_model=SpaceResponse)
def create_space(space: SpaceCreate, db: Session = Depends(get_db)):
    db_space = Space(**space.dict())
    db.add(db_space)
    db.commit()
    db.refresh(db_space)
    return db_space

# Obtener todos los espacios
@router.get("/spaces", response_model=list[SpaceResponse])
def get_spaces(db: Session = Depends(get_db)):
    return db.query(Space).all()

spaces = [
    {"name": "Sala A", "capacity": 20},
    {"name": "Sala B", "capacity": 50},
    {"name": "Auditorio", "capacity": 100},
    {"name": "Espacio Abierto", "capacity": 200}
]

@router.get("/api/recommend/space/{num_attendees}")
def recommend_space(num_attendees: int):
    suitable_spaces = [s for s in spaces if s["capacity"] >= num_attendees]
    
    if not suitable_spaces:
        return {"message": "No hay espacios adecuados para este número de asistentes"}
    
    return {"space": random.choice(suitable_spaces)["name"]}