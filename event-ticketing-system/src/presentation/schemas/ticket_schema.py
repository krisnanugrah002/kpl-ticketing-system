from pydantic import BaseModel
import uuid

class CheckInRequest(BaseModel):
    event_id: uuid.UUID
    ticket_code: str