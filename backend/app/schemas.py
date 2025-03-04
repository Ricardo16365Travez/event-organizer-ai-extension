from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Esquema de Usuario
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True  # Compatibilidad con SQLAlchemy

# Esquema de Evento
class EventCreate(BaseModel):
    name: str
    event_type: str
    date: datetime

class EventResponse(BaseModel):
    id: int
    name: str
    event_type: str
    date: datetime

    class Config:
        from_attributes = True

# Esquema de Agenda
class AgendaCreate(BaseModel):
    event_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class AgendaResponse(BaseModel):
    id: int
    event_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True

# Esquema de Speaker
class SpeakerCreate(BaseModel):
    name: str
    topic: str

class SpeakerResponse(BaseModel):
    id: int
    name: str
    topic: str

    class Config:
        from_attributes = True


class SpaceCreate(BaseModel):
    name: str
    location: str
    capacity: int

class SpaceResponse(BaseModel):
    id: int
    name: str
    location: str
    capacity: int

    class Config:
        from_attributes = True

class ReportCreate(BaseModel):
    event_id: int
    rating: int
    organization: int
    speaker_quality: int
    venue_satisfaction: int
    engagement: int
    logistics: int
    feedback: str

    class Config:
        from_attributes = True


class ReportResponse(ReportCreate):
    id: int
    ai_analysis: Optional[str] = None