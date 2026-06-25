from dataclasses import dataclass
import uuid

@dataclass
class GetPurchasedTicketsQuery:
    customer_id: uuid.UUID