import random
import joblib
from app.models import Speaker, Space
from sqlalchemy.orm import Session

def recommend_speaker(db: Session, event_type: str):
    speakers = db.query(Speaker).filter(Speaker.topic == event_type).all()
    return random.choice(speakers) if speakers else None

def recommend_space(db: Session, num_attendees: int):
    spaces = db.query(Space).filter(Space.capacity >= num_attendees).all()
    return random.choice(spaces) if spaces else None

def train_speaker_model(db: Session):
    speakers = db.query(Speaker).all()
    data = [(s.name, s.topic) for s in speakers]
    model = {topic: [] for _, topic in data}
    for name, topic in data:
        model[topic].append(name)
    joblib.dump(model, "speaker_model.pkl")

def predict_speaker(event_type: str):
    model = joblib.load("speaker_model.pkl")
    return model.get(event_type, ["No hay recomendación disponible"])[0]
