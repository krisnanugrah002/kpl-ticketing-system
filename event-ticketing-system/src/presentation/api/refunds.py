import uuid
from fastapi import APIRouter, Depends, HTTPException

from src.application.commands.approve_refund_command import ApproveRefundCommand
from src.application.command_handlers.approve_refund_handler import ApproveRefundHandler
from src.presentation.dependencies import get_approve_refund_handler

router = APIRouter(prefix="/refunds", tags=["Refunds"])

@router.post("/{id}/approve")
def approve_refund(
    id: uuid.UUID, 
    handler: ApproveRefundHandler = Depends(get_approve_refund_handler)
):
    try:
        command = ApproveRefundCommand(refund_id=id)
        handler.handle(command)
        return {"message": "Refund approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))