import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

@dataclass(frozen=True)
class RefundRequested:
    refund_id: uuid.UUID
    booking_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class RefundApproved:
    refund_id: uuid.UUID
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class RefundRejected:
    refund_id: uuid.UUID
    reason: str
    occurred_on: datetime = field(default_factory=get_utc_now)

@dataclass(frozen=True)
class RefundPaidOut:
    refund_id: uuid.UUID
    payment_reference: str
    occurred_on: datetime = field(default_factory=get_utc_now)