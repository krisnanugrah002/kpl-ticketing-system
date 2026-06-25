import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.database.models.base import Base

class TicketModel(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id = Column(UUID(as_uuid=True), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    event_id = Column(UUID(as_uuid=True), nullable=False)
    category_id = Column(UUID(as_uuid=True), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)