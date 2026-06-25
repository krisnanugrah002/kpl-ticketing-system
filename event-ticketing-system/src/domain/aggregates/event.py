import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import List
from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange

class EventStatus(Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

@dataclass
class Event:
    id: uuid.UUID
    name: str
    description: str
    location: str
    max_capacity: int
    date_range: DateRange
    status: EventStatus = field(default=EventStatus.DRAFT)
    categories: List[TicketCategory] = field(default_factory=list)
    domain_events: List = field(default_factory=list)

    def __post_init__(self):
        if self.max_capacity <= 0:
            raise ValueError("Maximum capacity must be greater than zero.")

    def add_ticket_category(self, category: TicketCategory):
        if category.sales_period.end_date > self.date_range.start_date:
            raise ValueError("Ticket sales period must end before or on the event start date.")

        current_total_quota = sum(cat.quota for cat in self.categories)
        if current_total_quota + category.quota > self.max_capacity:
            raise ValueError("Total ticket quota exceeds event maximum capacity.")

        self.categories.append(category)

    def publish(self):
        if self.status == EventStatus.CANCELLED:
            raise ValueError("Cancelled events cannot be published.")

        active_categories = [cat for cat in self.categories if cat.is_active]
        if not active_categories:
            raise ValueError("Event must have at least one active ticket category to be published.")

        total_quota = sum(cat.quota for cat in self.categories)
        if total_quota > self.max_capacity:
            raise ValueError("Total ticket quota exceeds event capacity.")

        self.status = EventStatus.PUBLISHED
        
    def cancel(self):
        if self.status == EventStatus.COMPLETED:
            raise ValueError("Completed events cannot be cancelled.")
        
        self.status = EventStatus.CANCELLED
        
        for category in self.categories:
            category.deactivate()

    def complete_event(self):
        self.status = EventStatus.COMPLETED

    @property
    def total_reserved_quota(self) -> int:
        return sum(cat.quota for cat in self.categories)
    
    def disable_category(self, category_id: uuid.UUID) -> None:
        category = next((c for c in self.categories if c.id == category_id), None)
        if not category:
            raise ValueError("Ticket category not found in this event.")
        
        if hasattr(category, 'disable'):
            category.disable()
        elif hasattr(category, 'is_active'):
            category.is_active = False
        else:
            category.status = "Disabled"