from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, CheckConstraint
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


class Event(Base):
    __tablename__ = "event"
    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    venue_id = Column(UUID(as_uuid=True), ForeignKey("content.venue.id"), nullable=False)
    title = Column(String(80), nullable=False)
    hour_change = Column(DateTime(timezone=True))
    starts_at = Column(DateTime(timezone=True))
    description = Column(String(500))
    min_price = Column(Float)
    total_capacity = Column(Integer, nullable=False, default=0)
    available = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    venue = relationship("Venue", back_populates="events")
    ticket_types = relationship("TicketType", back_populates="event", cascade="all, delete-orphan")


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

    event = relationship("Event", back_populates="ticket_types")
    tickets = relationship("Ticket", back_populates="ticket_type")


class Order(Base):
    __tablename__ = "order"
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'confirmed', 'cancelled')", name="chk_order_status"),
        {"schema": "content"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    total = Column(Float, nullable=False, default=0)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tickets = relationship("Ticket", back_populates="order", cascade="all, delete-orphan")


class Ticket(Base):
    __tablename__ = "ticket"
    __table_args__ = {"schema": "content"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("content.order.id"), nullable=False)
    ticket_type_id = Column(UUID(as_uuid=True), ForeignKey("content.ticket_type.id"), nullable=False)
    participant_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="tickets")
    ticket_type = relationship("TicketType", back_populates="tickets")