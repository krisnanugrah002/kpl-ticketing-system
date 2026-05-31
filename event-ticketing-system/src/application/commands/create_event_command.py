from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class TicketCategoryCommandData:
    name: str
    price: float
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime

@dataclass
class CreateEventCommand:
    name: str
    description: str
    location: str
    max_capacity: int
    start_date: datetime
    end_date: datetime
    categories: List[TicketCategoryCommandData]