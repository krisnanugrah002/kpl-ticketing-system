from pydantic import BaseModel
import uuid

class CreateBookingRequest(BaseModel):
    customer_id: uuid.UUID
    event_id: uuid.UUID
    ticket_category_id: uuid.UUID
    quantity: int

class PayBookingRequest(BaseModel):
    payment_amount: float