from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Event
from datetime import datetime
from app.schemas import EventCreate, EventResponse,SpeakerCreate, SpeakerResponse

router = APIRouter()

@router.post("/api/events")
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # Verificar que no haya otro evento en la misma fecha y hora
    conflict = db.query(Event).filter(Event.date == event.date).first()
    if conflict:
        raise HTTPException(status_code=400, detail="Ya hay un evento programado en esta fecha y hora")

    new_event = Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/api/events", response_model=list[EventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@router.delete("/api/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    db.delete(event)
    db.commit()
    return {"message": "Evento eliminado"}

@router.put("/api/events/{event_id}")
def edit_event(event_id: int, event_update: EventCreate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    if datetime.now() >= event.date:
        raise HTTPException(status_code=400, detail="No se puede editar un evento que ya comenzó")

    event.name = event_update.name
    event.event_type = event_update.event_type
    event.date = event_update.date

    db.commit()
    return {"message": "Evento actualizado con éxito"}