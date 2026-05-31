import uuid
from dataclasses import dataclass

@dataclass
class ParticipantDTO:
    ticket_id: uuid.UUID
    ticket_code: str
    category_name: str
    status: str