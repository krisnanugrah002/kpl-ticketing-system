import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class TicketCreated:
    ticket_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class TicketCheckedIn:
    ticket_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class TicketCancelled:
    ticket_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)