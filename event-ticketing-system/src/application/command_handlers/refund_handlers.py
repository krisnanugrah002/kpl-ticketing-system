from src.application.commands.refund_commands import RequestRefundCommand, RejectRefundCommand, MarkRefundPaidOutCommand
from src.domain.repositories.refund_repository import RefundRepository
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.ticket_repository import TicketRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.aggregates.refund import Refund

class RequestRefundHandler:
    def __init__(self, refund_repo: RefundRepository, booking_repo: BookingRepository, ticket_repo: TicketRepository, event_repo: EventRepository):
        self.refund_repo = refund_repo
        self.booking_repo = booking_repo
        self.ticket_repo = ticket_repo
        self.event_repo = event_repo

    def handle(self, command: RequestRefundCommand) -> uuid.UUID:
        booking = self.booking_repo.get_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking not found.")
        
        existing_refund = self.refund_repo.get_by_booking_id(command.booking_id)
        if existing_refund:
            raise ValueError("Refund already requested for this booking.")

        tickets = self.ticket_repo.get_by_booking_id(booking.id)
        event = self.event_repo.get_by_id(booking.event_id)
       
        refund_deadline = event.date_range.start_date
        
        refund = Refund.create(booking, tickets, refund_deadline, command.current_time)
        self.refund_repo.save(refund)
        return refund.id

class RejectRefundHandler:
    def __init__(self, refund_repo: RefundRepository):
        self.refund_repo = refund_repo

    def handle(self, command: RejectRefundCommand) -> None:
        refund = self.refund_repo.get_by_id(command.refund_id)
        if not refund:
            raise ValueError("Refund not found.")
        refund.reject(command.reason)
        self.refund_repo.save(refund)

class MarkRefundPaidOutHandler:
    def __init__(self, refund_repo: RefundRepository):
        self.refund_repo = refund_repo

    def handle(self, command: MarkRefundPaidOutCommand) -> None:
        refund = self.refund_repo.get_by_id(command.refund_id)
        if not refund:
            raise ValueError("Refund not found.")
        refund.mark_as_paid_out(command.payment_reference)
        self.refund_repo.save(refund)