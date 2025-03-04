from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    events = relationship("Event", back_populates="organizer")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    event_type = Column(String)
    organizer_id = Column(Integer, ForeignKey("users.id"))

    organizer = relationship("User", back_populates="events")
    speakers = relationship("Speaker", back_populates="event")
    agendas = relationship("Agenda", back_populates="event")
    spaces = relationship("Space", back_populates="event")
    reports = relationship("Report", back_populates="event")

class Speaker(Base):
    __tablename__ = "speakers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    topic = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="speakers")

class Agenda(Base):
    __tablename__ = "agendas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="agendas")

class Space(Base):
    __tablename__ = "spaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="spaces")

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    organization = Column(Integer, nullable=False)
    speaker_quality = Column(Integer, nullable=False)
    venue_satisfaction = Column(Integer, nullable=False)
    engagement = Column(Integer, nullable=False)
    logistics = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=False)
    ai_analysis = Column(Text, nullable=True)  # Almacena la retroalimentación generada por IA

    event = relationship("Event", back_populates="reports")
