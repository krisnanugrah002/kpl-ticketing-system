import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException

from src.presentation.schemas.refund_schema import RequestRefundRequest, RejectRefundRequest, MarkPaidOutRequest
from src.application.commands.refund_commands import RequestRefundCommand, RejectRefundCommand, MarkRefundPaidOutCommand
from src.application.commands.approve_refund_command import ApproveRefundCommand
from src.application.command_handlers.refund_handlers import RequestRefundHandler, RejectRefundHandler, MarkRefundPaidOutHandler
from src.presentation.dependencies import get_refund_repository, get_booking_repository, get_ticket_repository, get_event_repository, get_approve_refund_handler
from src.application.command_handlers.approve_refund_handler import ApproveRefundHandler

router = APIRouter(prefix="/refunds", tags=["Refunds"])

def get_request_refund_handler(
    refund_repo=Depends(get_refund_repository), booking_repo=Depends(get_booking_repository),
    ticket_repo=Depends(get_ticket_repository), event_repo=Depends(get_event_repository)
):
    return RequestRefundHandler(refund_repo, booking_repo, ticket_repo, event_repo)

def get_reject_refund_handler(refund_repo=Depends(get_refund_repository)):
    return RejectRefundHandler(refund_repo)

def get_mark_paid_out_handler(refund_repo=Depends(get_refund_repository)):
    return MarkRefundPaidOutHandler(refund_repo)

@router.post("/request")
def request_refund(
    request: RequestRefundRequest, 
    handler: RequestRefundHandler = Depends(get_request_refund_handler)
):
    try:
        command = RequestRefundCommand(booking_id=request.booking_id, current_time=datetime.now(timezone.utc))
        refund_id = handler.handle(command)
        return {"refund_id": refund_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id}/approve")
def approve_refund(id: uuid.UUID, handler: ApproveRefundHandler = Depends(get_approve_refund_handler)):
    try:
        handler.handle(ApproveRefundCommand(refund_id=id))
        return {"message": "Refund approved successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id}/reject")
def reject_refund(id: uuid.UUID, request: RejectRefundRequest, handler: RejectRefundHandler = Depends(get_reject_refund_handler)):
    try:
        handler.handle(RejectRefundCommand(refund_id=id, reason=request.reason))
        return {"message": "Refund rejected"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id}/payout")
def mark_paid_out(id: uuid.UUID, request: MarkPaidOutRequest, handler: MarkRefundPaidOutHandler = Depends(get_mark_paid_out_handler)):
    try:
        handler.handle(MarkRefundPaidOutCommand(refund_id=id, payment_reference=request.payment_reference))
        return {"message": "Refund marked as paid out"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))