import uuid
from typing import List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TicketCategoryDTO:
    id: uuid.UUID
    name: str
    price: float
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime
    is_active: bool

@dataclass
class EventDTO:
    id: uuid.UUID
    name: str
    description: str
    location: str
    max_capacity: int
    start_date: datetime
    end_date: datetime
    status: str
    categories: List[TicketCategoryDTO]