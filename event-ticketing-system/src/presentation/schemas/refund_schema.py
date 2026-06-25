from pydantic import BaseModel
import uuid

class RequestRefundRequest(BaseModel):
    booking_id: uuid.UUID

class RejectRefundRequest(BaseModel):
    reason: str

class MarkPaidOutRequest(BaseModel):
    payment_reference: str