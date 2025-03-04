from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Speaker
from app.schemas import SpeakerResponse
import random
import openai 
from app.config import OPENAI_API_KEY 
from sentence_transformers import SentenceTransformer

router = APIRouter()


openai.api_key = "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"  


SPEAKER_DATABASE = [
    {"name": "Carlos Pérez", "topic": "BodasRecepciones", "available": True},
    {"name": "María González", "topic": "EventosCorporativos", "available": True},
    {"name": "Luis Herrera", "topic": "FiestasPrivadas", "available": False},
    {"name": "Ana Rojas", "topic": "EventosCulturales", "available": True},
    {"name": "Javier Salazar", "topic": "EventosCorporativos", "available": True},
    {"name": "Elena Méndez", "topic": "BodasRecepciones", "available": True},
    {"name": "Pedro Ramírez", "topic": "FiestasPrivadas", "available": False},
]

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_speaker_embedding(event_type: str):
    return model.encode(event_type).tolist()

@router.get("/api/recommend/speaker/{event_type}")
def recommend_speaker(event_type: str):
    available_speakers = [s for s in SPEAKER_DATABASE if s["available"]]

    if not available_speakers:
        raise HTTPException(status_code=404, detail="No hay speakers disponibles en este momento.")

    # Obtener embedding del evento
    event_embedding = get_speaker_embedding(event_type)

    # Buscar el speaker con el embedding más cercano
    best_match = None
    best_score = float("-inf")

    for speaker in available_speakers:
        speaker_embedding = get_speaker_embedding(speaker["topic"])
        similarity = sum(a * b for a, b in zip(event_embedding, speaker_embedding))  # Producto punto
        if similarity > best_score:
            best_score = similarity
            best_match = speaker

    if best_match:
        return {"speaker": best_match["name"]}
    else:
        return {"message": "No se encontró un speaker adecuado para este evento."}
