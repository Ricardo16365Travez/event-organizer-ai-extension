from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base

# Modelo de Usuario
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    events = relationship("Event", back_populates="organizer")

# Modelo de Evento
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)  # Usar DateTime en lugar de String para fechas
    location = Column(String)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Clave foránea con User

    organizer = relationship("User", back_populates="events")
    speakers = relationship("Speaker", back_populates="event", cascade="all, delete")
    agendas = relationship("Agenda", back_populates="event", cascade="all, delete")
    spaces = relationship("Space", back_populates="event", cascade="all, delete")

# Modelo de Speaker (Orador)
class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    topic = Column(Text)  # Permitir descripciones largas
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="speakers")

# Modelo de Agenda
class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="agendas")

# Modelo de Espacio
class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    capacity = Column(Integer)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="spaces")
