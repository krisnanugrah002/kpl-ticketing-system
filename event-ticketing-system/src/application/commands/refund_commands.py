import uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RequestRefundCommand:
    booking_id: uuid.UUID
    current_time: datetime

@dataclass
class RejectRefundCommand:
    refund_id: uuid.UUID
    reason: str

@dataclass
class MarkRefundPaidOutCommand:
    refund_id: uuid.UUID
    payment_reference: str