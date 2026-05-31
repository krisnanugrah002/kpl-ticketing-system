import uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class CheckInCommand:
    event_id: uuid.UUID
    ticket_code: str
    current_time: datetime