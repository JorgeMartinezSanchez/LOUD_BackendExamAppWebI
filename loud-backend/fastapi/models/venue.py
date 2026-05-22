from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Venue(Base):
    __tablename__ = "venue"
    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    events = relationship("Event", back_populates="venue", cascade="all, delete-orphan")