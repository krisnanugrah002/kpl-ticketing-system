import uuid
from src.application.commands.pay_booking_command import PayBookingCommand
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.ticket_repository import TicketRepository
from src.application.interfaces.payment_gateway import PaymentGateway
from src.domain.aggregates.ticket import Ticket
from src.domain.value_objects.ticket_code import TicketCode

class PayBookingHandler:
    def __init__(
        self, 
        booking_repository: BookingRepository, 
        ticket_repository: TicketRepository,
        payment_gateway: PaymentGateway
    ):
        self.booking_repository = booking_repository
        self.ticket_repository = ticket_repository
        self.payment_gateway = payment_gateway

    def handle(self, command: PayBookingCommand) -> None:
        booking = self.booking_repository.get_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        # Proses pembayaran via pihak eksternal
        payment_success = self.payment_gateway.process_payment(command.booking_id, command.payment_amount)
        if not payment_success:
            raise ValueError("Payment failed at gateway.")

        # Ubah status booking di Domain
        booking.pay(command.payment_amount)
        self.booking_repository.save(booking)

        # Terbitkan tiket baru
        for _ in range(booking.quantity):
            ticket = Ticket(
                id=uuid.uuid4(),
                booking_id=booking.id,
                event_id=booking.event_id,
                category_id=booking.ticket_category_id,
                code=TicketCode()
            )
            self.ticket_repository.save(ticket)