import uuid
from dataclasses import dataclass

@dataclass
class CreateBookingCommand:
    customer_id: uuid.UUID
    event_id: uuid.UUID
    ticket_category_id: uuid.UUID
    quantity: int