import pytest
import uuid
from datetime import datetime, timedelta, timezone
from src.domain.aggregates.booking import Booking, BookingStatus
from src.domain.aggregates.ticket import Ticket, TicketStatus
from src.domain.aggregates.refund import Refund, RefundStatus
from src.domain.value_objects.money import Money
from src.domain.value_objects.ticket_code import TicketCode

def setup_mock_booking(status: BookingStatus) -> Booking:
    booking = Booking(
        customer_id=uuid.uuid4(),
        event_id=uuid.uuid4(),
        ticket_category_id=uuid.uuid4(),
        quantity=1,
        total_price=Money(150000),
        payment_deadline=datetime.now(timezone.utc) + timedelta(hours=2)
    )
    booking.status = status
    return booking

def test_refund_fails_when_ticket_already_checked_in():
    """
    Menguji BR39: Refund gagal dibuat jika ada tiket yang statusnya CheckedIn.
    """
    booking = setup_mock_booking(BookingStatus.PAID)
    
    checked_in_ticket = Ticket(
        id=uuid.uuid4(),
        booking_id=booking.id,
        event_id=booking.event_id,
        category_id=booking.ticket_category_id,
        code=TicketCode(),
        status=TicketStatus.CHECKED_IN
    )
    
    current_time = datetime.now(timezone.utc)
    deadline = current_time + timedelta(days=1)

    with pytest.raises(ValueError, match="Cannot request a refund if any associated ticket has already been checked in."):
        Refund.create(
            booking=booking,
            associated_tickets=[checked_in_ticket],
            refund_deadline=deadline,
            current_time=current_time
        )

def test_refund_fails_when_booking_is_not_paid():
    """Menguji BR38: Refund harus berasal dari booking yang Paid."""
    booking = setup_mock_booking(BookingStatus.PENDING_PAYMENT)
    current_time = datetime.now(timezone.utc)
    deadline = current_time + timedelta(days=1)

    with pytest.raises(ValueError, match="Refund can only be requested for a Paid booking."):
        Refund.create(booking, [], deadline, current_time)

def test_refund_fails_after_deadline():
    """Menguji BR40: Gagal jika melewati deadline."""
    booking = setup_mock_booking(BookingStatus.PAID)
    current_time = datetime.now(timezone.utc)
    expired_deadline = current_time - timedelta(minutes=10)

    with pytest.raises(ValueError, match="Refund request has passed the allowed deadline."):
        Refund.create(booking, [], expired_deadline, current_time)

def test_refund_approve_and_reject_flow():
    """Menguji BR41, BR44, BR45: Transisi approve dan reject."""
    booking = setup_mock_booking(BookingStatus.PAID)
    current_time = datetime.now(timezone.utc)
    deadline = current_time + timedelta(days=1)
    
    # 1. Test Approve
    refund1 = Refund.create(booking, [], deadline, current_time)
    refund1.approve()
    assert refund1.status == RefundStatus.APPROVED

    # 2. Test Reject wajib alasan
    refund2 = Refund.create(booking, [], deadline, current_time)
    with pytest.raises(ValueError, match="reason must be provided"):
        refund2.reject("")
        
    refund2.reject("Invalid document proof.")
    assert refund2.status == RefundStatus.REJECTED
    assert refund2.rejection_reason == "Invalid document proof."

def test_mark_as_paid_out_success():
    """Menguji BR47, BR48, BR49: Transisi status ke PaidOut."""
    booking = setup_mock_booking(BookingStatus.PAID)
    current_time = datetime.now(timezone.utc)
    deadline = current_time + timedelta(days=1)
    
    refund = Refund.create(booking, [], deadline, current_time)
    refund.approve()
    
    refund.mark_as_paid_out("PAY-REF-99102")
    assert refund.status == RefundStatus.PAID_OUT
    assert refund.payment_reference == "PAY-REF-99102"