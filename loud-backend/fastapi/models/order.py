from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

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

    # Relaciones
    tickets = relationship("Ticket", back_populates="order", cascade="all, delete-orphan")