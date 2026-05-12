from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class BookingReserved:
    booking_id: UUID
    event_id: UUID
    customer_id: UUID
    quantity: int
    reserved_at: datetime

@dataclass(frozen=True)
class BookingPaid:
    booking_id: UUID
    paid_at: datetime

@dataclass(frozen=True)
class BookingExpired:
    booking_id: UUID
    event_id: UUID
    released_quantity: int