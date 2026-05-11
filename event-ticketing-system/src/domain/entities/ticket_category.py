import uuid
from dataclasses import dataclass, field
from src.domain.value_objects.money import Money
from src.domain.value_objects.date_range import DateRange

@dataclass
class TicketCategory:
    id: uuid.UUID
    name: str
    price: Money
    quota: int
    sales_period: DateRange
    is_active: bool = field(default=True)

    def __post_init__(self):
        if self.quota <= 0:
            raise ValueError("Ticket quota must be greater than zero.")

    def deactivate(self):
        self.is_active = False

    def decrease_quota(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Decrease quantity must be greater than zero.")
        if self.quota < quantity:
            raise ValueError("Not enough ticket quota available.")
        
        self.quota -= quantity

    def increase_quota(self, quantity: int):
        if quantity <= 0:
            raise ValueError("Increase quantity must be greater than zero.")
        
        self.quota += quantity