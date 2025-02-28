from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Agenda
from ..schemas import AgendaCreate, AgendaResponse  

router = APIRouter()

# Crear una agenda
@router.post("/agendas", response_model=AgendaResponse)
def create_agenda(agenda: AgendaCreate, db: Session = Depends(get_db)):
    db_agenda = Agenda(**agenda.dict())
    db.add(db_agenda)
    db.commit()
    db.refresh(db_agenda)
    return db_agenda

# Obtener todas las agendas
@router.get("/agendas", response_model=list[AgendaResponse])
def get_agendas(db: Session = Depends(get_db)):
    return db.query(Agenda).all()

# Obtener una agenda por ID
@router.get("/agendas/{agenda_id}", response_model=AgendaResponse)
def get_agenda(agenda_id: int, db: Session = Depends(get_db)):
    agenda = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not agenda:
        raise HTTPException(status_code=404, detail="Agenda no encontrada")
    return agenda

# Eliminar una agenda
@router.delete("/agendas/{agenda_id}")
def delete_agenda(agenda_id: int, db: Session = Depends(get_db)):
    agenda = db.query(Agenda).filter(Agenda.id == agenda_id).first()
    if not agenda:
        raise HTTPException(status_code=404, detail="Agenda no encontrada")
    
    db.delete(agenda)
    db.commit()
    return {"message": "Agenda eliminada"}
