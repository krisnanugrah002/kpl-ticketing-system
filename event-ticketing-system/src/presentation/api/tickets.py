from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone

from src.presentation.schemas.ticket_schema import CheckInRequest
from src.application.commands.check_in_command import CheckInCommand
from src.application.command_handlers.check_in_handler import CheckInHandler
from src.presentation.dependencies import get_check_in_handler

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