from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class TicketType(Base):
    __tablename__ = "ticket_type"
    __table_args__ = (
        CheckConstraint("available >= 0 AND available <= total_capacity", name="chk_ticket_type_available"),
        {"schema": "content"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("content.event.id"), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    total_capacity = Column(Integer, nullable=False, default=0)
    available = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())