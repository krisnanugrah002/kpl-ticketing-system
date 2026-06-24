from src.application.commands.expire_booking_command import ExpireBookingCommand
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.repositories.event_repository import EventRepository
from src.domain.aggregates.booking import BookingStatus

class ExpireBookingHandler:
    def __init__(self, booking_repo: BookingRepository, event_repo: EventRepository):
        self.booking_repo = booking_repo
        self.event_repo = event_repo

    def handle(self, command: ExpireBookingCommand) -> None:
        booking = self.booking_repo.get_by_id(command.booking_id)
        if not booking:
            raise ValueError("Booking not found.")

        if booking.status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("Only pending bookings can be expired.")

        if command.current_time <= booking.payment_deadline:
            raise ValueError("Payment deadline has not passed yet.")

        booking.status = BookingStatus.EXPIRED
        self.booking_repo.save(booking)

        event = self.event_repo.get_by_id(booking.event_id)
        if event:
            for category in event.categories:
                if category.id == booking.ticket_category_id:
                    category.quota += booking.quantity
            self.event_repo.save(event)