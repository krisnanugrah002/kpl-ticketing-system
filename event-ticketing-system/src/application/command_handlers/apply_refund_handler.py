from src.application.commands.approve_refund_command import ApproveRefundCommand
from src.domain.repositories.refund_repository import RefundRepository
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.ticket_repository import TicketRepository
from src.domain.aggregates.booking import BookingStatus

class ApproveRefundHandler:
    def __init__(
        self, 
        refund_repository: RefundRepository,
        booking_repository: BookingRepository,
        ticket_repository: TicketRepository
    ):
        self.refund_repository = refund_repository
        self.booking_repository = booking_repository
        self.ticket_repository = ticket_repository

    def handle(self, command: ApproveRefundCommand) -> None:
        refund = self.refund_repository.get_by_id(command.refund_id)
        if not refund:
            raise ValueError("Refund not found.")

        booking = self.booking_repository.get_by_id(refund.booking_id)
        tickets = self.ticket_repository.get_by_booking_id(booking.id)

        refund.approve()

        booking.status = BookingStatus.REFUNDED

        for ticket in tickets:
            ticket.cancel()
            self.ticket_repository.save(ticket)

        self.booking_repository.save(booking)
        self.refund_repository.save(refund)