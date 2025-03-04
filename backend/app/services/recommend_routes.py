from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.recommendation import recommend_speaker, recommend_space, predict_speaker

router = APIRouter()

@router.get("/api/recommend/speaker/{event_type}")
def get_speaker(event_type: str, db: Session = Depends(get_db)):
    speaker = recommend_speaker(db, event_type)
    return {"speaker": speaker.name if speaker else predict_speaker(event_type)}

@router.get("/api/recommend/space/{num_attendees}")
def get_space(num_attendees: int, db: Session = Depends(get_db)):
    space = recommend_space(db, num_attendees)
    return {"space": space.name if space else "No hay espacios disponibles"}
