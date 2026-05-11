import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class EventCreated:
    event_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class EventPublished:
    event_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class EventCancelled:
    event_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class TicketCategoryCreated:
    event_id: uuid.UUID
    ticket_category_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class TicketCategoryDisabled:
    event_id: uuid.UUID
    ticket_category_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)