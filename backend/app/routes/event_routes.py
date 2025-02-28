from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Event
from ..schemas import EventCreate, EventResponse

router = APIRouter()

# Crear un evento
@router.post("/events", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    db_event = Event(**event.dict())  # No usamos `location` porque no está en `EventCreate`
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# Obtener todos los eventos
@router.get("/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

# Obtener un evento por ID
@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return event

# Eliminar un evento
@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.delete(event)
    db.commit()
    return {"message": "Evento eliminado"}
