from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import Session

from src.presentation.dependencies import get_check_in_handler, get_session
from src.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from src.application.query_handlers.get_purchased_tickets_handler import GetPurchasedTicketsHandler

from src.presentation.schemas.ticket_schema import CheckInRequest
from src.application.commands.check_in_command import CheckInCommand
from src.application.command_handlers.check_in_handler import CheckInHandler

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/check-in")
def check_in_ticket(
    request: CheckInRequest,
    handler: CheckInHandler = Depends(get_check_in_handler)
):
    try:
        current_time = datetime.now(timezone.utc)
        command = CheckInCommand(
            event_id=request.event_id,
            ticket_code=request.ticket_code,
            current_time=current_time
        )
        handler.handle(command)
        return {"message": "Check-in successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/purchased/{booking_id}", status_code=status.HTTP_200_OK)
def get_purchased_tickets(
    booking_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    try:
        handler = GetPurchasedTicketsHandler(session)
        query = GetPurchasedTicketsQuery(booking_id=booking_id)
        tickets = handler.handle(query)
        return {"tickets": tickets}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))