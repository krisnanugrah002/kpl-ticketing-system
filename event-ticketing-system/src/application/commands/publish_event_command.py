import uuid
from dataclasses import dataclass

@dataclass
class PublishEventCommand:
    event_id: uuid.UUID