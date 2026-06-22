import uuid
from fastapi import APIRouter, Depends, HTTPException
from decimal import Decimal

from src.presentation.schemas.booking_schema import CreateBookingRequest, PayBookingRequest
from src.application.commands.create_booking_command import CreateBookingCommand
from src.application.commands.pay_booking_command import PayBookingCommand
from src.application.command_handlers.create_booking_handler import CreateBookingHandler
from src.application.command_handlers.pay_booking_handler import PayBookingHandler
from src.domain.value_objects.money import Money
from src.presentation.dependencies import get_create_booking_handler, get_pay_booking_handler

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/")
def create_booking(
    request: CreateBookingRequest, 
    handler: CreateBookingHandler = Depends(get_create_booking_handler)
):
    try:
        command = CreateBookingCommand(
            customer_id=request.customer_id,
            event_id=request.event_id,
            ticket_category_id=request.ticket_category_id,
            quantity=request.quantity
        )
        booking_id = handler.handle(command)
        return {"booking_id": booking_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{id}/pay")
def pay_booking(
    id: uuid.UUID, 
    request: PayBookingRequest, 
    handler: PayBookingHandler = Depends(get_pay_booking_handler)
):
    try:
        amount = Money(Decimal(str(request.payment_amount)))
        command = PayBookingCommand(booking_id=id, payment_amount=amount)
        handler.handle(command)
        return {"message": "Payment successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))