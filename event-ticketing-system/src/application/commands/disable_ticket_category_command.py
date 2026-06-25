from dataclasses import dataclass
import uuid

@dataclass
class DisableTicketCategoryCommand:
    event_id: uuid.UUID
    category_id: uuid.UUID