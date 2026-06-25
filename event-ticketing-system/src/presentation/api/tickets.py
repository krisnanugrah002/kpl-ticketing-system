import uuid
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone

from src.presentation.schemas.ticket_schema import CheckInRequest
from src.application.commands.check_in_command import CheckInCommand
from src.application.command_handlers.check_in_handler import CheckInHandler
from src.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from src.application.query_handlers.get_purchased_tickets_handler import GetPurchasedTicketsHandler
from src.presentation.dependencies import get_check_in_handler, get_purchased_tickets_handler

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

@router.get("/purchased")
def get_purchased_tickets(
    customer_id: uuid.UUID,
    handler: GetPurchasedTicketsHandler = Depends(get_purchased_tickets_handler)
):
    try:
        query = GetPurchasedTicketsQuery(customer_id=customer_id)
        tickets = handler.handle(query)
        return tickets
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))