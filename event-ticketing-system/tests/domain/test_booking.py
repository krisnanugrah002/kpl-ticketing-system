import pytest
from uuid import uuid4
from datetime import datetime, timedelta, timezone
from src.domain.aggregates.booking import Booking, BookingStatus
from src.domain.value_objects.money import Money

def test_booking_fails_if_quantity_is_zero():
    """ BR21 """
    with pytest.raises(ValueError, match="greater than zero"):
        Booking(
            customer_id=uuid4(),
            event_id=uuid4(),
            ticket_category_id=uuid4(),
            quantity=0,  
            total_price=Money(100000),
            payment_deadline=datetime.now(timezone.utc) + timedelta(minutes=15)
        )

def test_booking_fails_payment_after_deadline():
    """ BR28 """
    past_deadline = datetime.now(timezone.utc) - timedelta(minutes=1)
    booking = Booking(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=2,
        total_price=Money(200000),
        payment_deadline=past_deadline
    )

    with pytest.raises(ValueError, match="payment deadline has passed"):
        booking.pay(Money(200000))

def test_booking_fails_payment_with_incorrect_amount():
    """ BR29 """
    total_price = Money(500000)
    booking = Booking(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=1,
        total_price=total_price,
        payment_deadline=datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    wrong_amount = Money(450000)
    with pytest.raises(ValueError, match="equal the total price"):
        booking.pay(wrong_amount)

def test_paid_booking_cannot_expire():
    """ BR31 """
    # 1. Setup booking dan bayar sukses
    total_price = Money(300000)
    booking = Booking(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=1,
        total_price=total_price,
        payment_deadline=datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    booking.pay(total_price)
    
    assert booking.status == BookingStatus.PAID

    # 2. Paksa panggil expire() meskipun sudah bayar
    with pytest.raises(ValueError, match="cannot be marked as expired"):
        booking.expire()

def test_booking_initial_status_is_pending():
    """ BR24 """
    booking = Booking(
        customer_id=uuid4(),
        event_id=uuid4(),
        ticket_category_id=uuid4(),
        quantity=1,
        total_price=Money(100000),
        payment_deadline=datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    assert booking.status == BookingStatus.PENDING_PAYMENT 