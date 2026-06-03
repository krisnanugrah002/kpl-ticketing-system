import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.infrastructure.database.models.base import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    location = Column(String(255), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False)

    categories = relationship("TicketCategoryModel", back_populates="event", cascade="all, delete-orphan")

class TicketCategoryModel(Base):
    __tablename__ = "ticket_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quota = Column(Integer, nullable=False)
    sales_start_date = Column(DateTime(timezone=True), nullable=False)
    sales_end_date = Column(DateTime(timezone=True), nullable=False)

    event = relationship("EventModel", back_populates="categories")