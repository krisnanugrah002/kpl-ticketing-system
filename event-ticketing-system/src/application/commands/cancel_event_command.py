from dataclasses import dataclass
import uuid

@dataclass
class CancelEventCommand:
    event_id: uuid.UUID