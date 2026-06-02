import uuid
from dataclasses import dataclass

@dataclass
class GetEventSalesReportQuery:
    event_id: uuid.UUID