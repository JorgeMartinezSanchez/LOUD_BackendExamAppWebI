from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Event(Base):
    __tablename__ = "event"
    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("content.venue.id"), nullable=False)
    title = Column(String(80), nullable=False)
    starts_at = Column(DateTime(timezone=True))
    description = Column(String(500))
    min_price = Column(Float)
    total_capacity = Column(Integer, nullable=False, default=0)
    available = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Estas relaciones se resolverán después de que todos los modelos estén cargados
    venue = relationship("Venue", back_populates="events")
    ticket_types = relationship("TicketType", back_populates="event", cascade="all, delete-orphan")