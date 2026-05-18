from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone
from src.domain.value_objects.money import Money

class BookingStatus(Enum):
    PENDING_PAYMENT = "PendingPayment"
    PAID = "Paid"
    EXPIRED = "Expired"
    REFUNDED = "Refunded"

class Booking:
    def __init__(
        self,
        customer_id: UUID,
        event_id: UUID,
        ticket_category_id: UUID,
        quantity: int,
        total_price: Money,
        payment_deadline: datetime,
        id: UUID = None
    ):
        if quantity <= 0:
            raise ValueError("The number of tickets in a booking must be greater than zero.")
        
        if total_price.amount < 0:
            raise ValueError("The total price must not be negative.")

        self.id = id or uuid4()
        self.customer_id = customer_id
        self.event_id = event_id
        self.ticket_category_id = ticket_category_id
        self.quantity = quantity
        self.total_price = total_price
        self.payment_deadline = payment_deadline
        
        self.status = BookingStatus.PENDING_PAYMENT
        self.created_at = datetime.now(timezone.utc)

    def pay(self, payment_amount: Money):

   
        if self.status != BookingStatus.PENDING_PAYMENT:
            raise ValueError("A booking can only be paid if its status is PendingPayment.")

        if datetime.now(timezone.utc) > self.payment_deadline:
            self.expire()
            raise ValueError("A booking cannot be paid if the payment deadline has passed.")

        if payment_amount != self.total_price:
            raise ValueError("The payment amount must equal the total price of the booking.")

        self.status = BookingStatus.PAID

    def expire(self):
       
        if self.status == BookingStatus.PAID:
            raise ValueError("A booking with a Paid status cannot be marked as expired.")
        
        if datetime.now(timezone.utc) > self.payment_deadline:
            self.status = BookingStatus.EXPIRED