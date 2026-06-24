from dataclasses import dataclass
import uuid

@dataclass
class GetPurchasedTicketsQuery:
    booking_id: uuid.UUID