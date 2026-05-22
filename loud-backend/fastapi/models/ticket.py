from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "ticket"
    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("content.order.id"), nullable=False)
    ticket_type_id = Column(UUID(as_uuid=True), ForeignKey("content.ticket_type.id"), nullable=False)
    participant_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())