import uuid
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from src.domain.value_objects.ticket_code import TicketCode

class TicketStatus(Enum):
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"

@dataclass
class Ticket:
    id: uuid.UUID
    booking_id: uuid.UUID
    event_id: uuid.UUID
    category_id: uuid.UUID
    code: TicketCode
    status: TicketStatus = field(default=TicketStatus.ACTIVE)
    domain_events: list = field(default_factory=list)

    def check_in(self, event_id: uuid.UUID, current_time: datetime):
        if self.event_id != event_id:
            raise ValueError("Ticket is not valid for this event.")
        
        if self.status == TicketStatus.CHECKED_IN:
            raise ValueError("Ticket has already been checked in.")
        
        if self.status == TicketStatus.CANCELLED:
            raise ValueError("Cannot check in a cancelled ticket.")

        self.status = TicketStatus.CHECKED_IN

    def cancel(self):
        if self.status == TicketStatus.CHECKED_IN:
            raise ValueError("Cannot cancel a ticket that has already been checked in.")
        
        self.status = TicketStatus.CANCELLED