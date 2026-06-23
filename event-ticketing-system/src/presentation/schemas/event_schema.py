from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid

class TicketCategoryCreate(BaseModel):
    name: str
    price: float
    quota: int
    sales_start_date: datetime
    sales_end_date: datetime

class EventCreate(BaseModel):
    name: str
    description: str
    location: str
    max_capacity: int
    start_date: datetime
    end_date: datetime
    categories: List[TicketCategoryCreate]