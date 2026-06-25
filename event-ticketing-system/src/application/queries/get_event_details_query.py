from dataclasses import dataclass
import uuid

@dataclass
class GetEventDetailsQuery:
    event_id: uuid.UUID