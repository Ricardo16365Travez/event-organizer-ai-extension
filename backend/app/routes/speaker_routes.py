from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Speaker
from ..schemas import SpeakerCreate, SpeakerResponse  

router = APIRouter()

# Crear un speaker
@router.post("/speakers", response_model=SpeakerResponse)
def create_speaker(speaker: SpeakerCreate, db: Session = Depends(get_db)):
    db_speaker = Speaker(**speaker.dict())
    db.add(db_speaker)
    db.commit()
    db.refresh(db_speaker)
    return db_speaker

# Obtener todos los speakers
@router.get("/speakers", response_model=list[SpeakerResponse])
def get_speakers(db: Session = Depends(get_db)):
    return db.query(Speaker).all()
