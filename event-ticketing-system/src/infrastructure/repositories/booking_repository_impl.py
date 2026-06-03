import uuid
from typing import Optional
from sqlalchemy.orm import Session
from src.domain.repositories.booking_repository import BookingRepository
from src.domain.aggregates.booking import Booking, BookingStatus
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.booking_model import BookingModel

class BookingRepositoryImpl(BookingRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, booking: Booking) -> None:
        model = self.session.query(BookingModel).filter_by(id=booking.id).first()
        if not model:
            model = BookingModel(id=booking.id)
            self.session.add(model)

        model.customer_id = booking.customer_id
        model.event_id = booking.event_id
        model.ticket_category_id = booking.ticket_category_id
        model.quantity = booking.quantity
        model.total_price = booking.total_price.amount
        model.status = booking.status.value
        model.payment_deadline = booking.payment_deadline
        model.created_at = booking.created_at
        self.session.commit()

    def get_by_id(self, booking_id: uuid.UUID) -> Optional[Booking]:
        model = self.session.query(BookingModel).filter_by(id=booking_id).first()
        if not model:
            return None

        booking = Booking(
            id=model.id,
            customer_id=model.customer_id,
            event_id=model.event_id,
            ticket_category_id=model.ticket_category_id,
            quantity=model.quantity,
            total_price=Money(model.total_price),
            payment_deadline=model.payment_deadline
        )
        booking.status = BookingStatus(model.status)
        booking.created_at = model.created_at
        return booking

    def get_active_booking_by_customer_event(self, customer_id: uuid.UUID, event_id: uuid.UUID) -> Optional[Booking]:
        model = self.session.query(BookingModel).filter(
            BookingModel.customer_id == customer_id,
            BookingModel.event_id == event_id,
            BookingModel.status.in_([BookingStatus.PENDING_PAYMENT.value, BookingStatus.PAID.value])
        ).first()
        return self.get_by_id(model.id) if model else None