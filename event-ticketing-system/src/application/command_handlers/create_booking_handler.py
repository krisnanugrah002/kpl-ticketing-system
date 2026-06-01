import uuid
from datetime import datetime, timedelta, timezone
from src.application.commands.create_booking_command import CreateBookingCommand
from src.domain.aggregates.booking import Booking
from src.domain.repositories.event_repository import EventRepository
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.value_objects.money import Money

class CreateBookingHandler:
    def __init__(self, event_repository: EventRepository, booking_repository: BookingRepository):
        self.event_repository = event_repository
        self.booking_repository = booking_repository

    def handle(self, command: CreateBookingCommand) -> uuid.UUID:
        event = self.event_repository.get_by_id(command.event_id)
        if not event:
            raise ValueError("Event not found.")

        category = next((c for c in event.categories if c.id == command.ticket_category_id), None)
        if not category:
            raise ValueError("Ticket category not found.")

        category.decrease_quota(command.quantity)

        total_price = category.price * command.quantity
        payment_deadline = datetime.now(timezone.utc) + timedelta(minutes=15)

        booking = Booking(
            id=uuid.uuid4(),
            customer_id=command.customer_id,
            event_id=command.event_id,
            ticket_category_id=command.ticket_category_id,
            quantity=command.quantity,
            total_price=total_price,
            payment_deadline=payment_deadline
        )

        # Simpan perubahan state pada Event (kuota berkurang) dan Booking baru
        self.event_repository.save(event)
        self.booking_repository.save(booking)

        return booking.id