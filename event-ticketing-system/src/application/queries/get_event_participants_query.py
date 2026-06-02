import uuid
from dataclasses import dataclass

@dataclass
class GetEventParticipantsQuery:
    event_id: uuid.UUID