from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Esquema de Usuario
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

# Esquema de Evento
class EventCreate(BaseModel):
    name: str
    description: str
    date: datetime
    organizer_id: int

class EventResponse(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    organizer_id: int

    class Config:
        from_attributes = True

# Esquema de Speaker (Corrección)
class SpeakerCreate(BaseModel):
    name: str
    bio: str
    expertise: str

class SpeakerResponse(SpeakerCreate):
    id: int

    class Config:
        from_attributes = True

# Esquema de Agenda
class AgendaCreate(BaseModel):
    event_id: int
    title: str
    description: str
    start_time: datetime
    end_time: datetime

class AgendaResponse(AgendaCreate):
    id: int

    class Config:
        from_attributes = True

# Esquema de Espacio (Corrección)
class SpaceCreate(BaseModel):
    name: str
    capacity: int

class SpaceResponse(SpaceCreate):
    id: int

    class Config:
        from_attributes = True
