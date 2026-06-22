from pydantic import BaseModel
import uuid

class CreateBookingRequest(BaseModel):
    customer_id: uuid.UUID
    event_id: uuid.UUID
    ticket_category_id: uuid.UUID
    quantity: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "customer_id": "123e4567-e89b-12d3-a456-426614174000",
                    "event_id": "987f6543-e21b-34c5-b678-426614174111",
                    "ticket_category_id": "555a4444-b12c-34d5-e678-426614174222",
                    "quantity": 2
                }
            ]
        }
    }

class PayBookingRequest(BaseModel):
    payment_amount: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "payment_amount": 150000.00
                }
            ]
        }
    }