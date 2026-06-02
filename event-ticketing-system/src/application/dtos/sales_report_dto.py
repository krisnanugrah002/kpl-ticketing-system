import uuid
from dataclasses import dataclass
from typing import Dict

@dataclass
class SalesReportDTO:
    event_id: uuid.UUID
    tickets_sold_per_category: Dict[str, int]
    total_pending_bookings: int
    total_paid_bookings: int
    total_expired_bookings: int
    total_refunded_bookings: int
    total_revenue: float