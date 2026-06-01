import uuid
from dataclasses import dataclass

@dataclass
class ApproveRefundCommand:
    refund_id: uuid.UUID