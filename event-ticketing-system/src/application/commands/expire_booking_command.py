import uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ExpireBookingCommand:
    booking_id: uuid.UUID
    current_time: datetime