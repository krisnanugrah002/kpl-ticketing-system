import uuid
from dataclasses import dataclass
from src.domain.value_objects.money import Money

@dataclass
class PayBookingCommand:
    booking_id: uuid.UUID
    payment_amount: Money