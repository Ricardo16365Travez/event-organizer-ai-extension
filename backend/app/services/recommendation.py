from ..models import Speaker
from sqlalchemy.orm import Session

def recommend_speaker(topic: str, db: Session):
    return db.query(Speaker).filter(Speaker.topic.ilike(f"%{topic}%")).all()
