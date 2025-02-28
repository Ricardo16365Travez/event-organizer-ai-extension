from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Space
from ..schemas import SpaceCreate, SpaceResponse  

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
