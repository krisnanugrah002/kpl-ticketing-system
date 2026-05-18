import pytest
import uuid
from datetime import datetime, timedelta

from src.domain.aggregates.event import Event, EventStatus
from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from decimal import Decimal

def create_valid_event_date() -> DateRange:
    start = datetime.now() + timedelta(days=30)
    end = start + timedelta(days=1)
    return DateRange(start_date=start, end_date=end)

def create_valid_sales_date(event_start: datetime) -> DateRange:
    start = datetime.now()
    end = event_start - timedelta(days=1)
    return DateRange(start_date=start, end_date=end)

def create_valid_ticket_category(quota: int, sales_period: DateRange) -> TicketCategory:
    return TicketCategory(
        id=uuid.uuid4(),
        name="Regular",
        price=Money(Decimal('100000.00')),
        quota=quota,
        sales_period=sales_period
    )



def test_create_event_success():
    event = Event(
        id=uuid.uuid4(),
        name="Konser Musik",
        description="Konser tahunan",
        location="Stadion",
        max_capacity=1000,
        date_range=create_valid_event_date()
    )
    
    assert event.max_capacity == 1000
    assert event.status == EventStatus.DRAFT

def test_create_event_fails_when_capacity_zero_or_negative():
    with pytest.raises(ValueError, match="Maximum capacity must be greater than zero."):
        Event(
            id=uuid.uuid4(),
            name="Konser Batal",
            description="Tes",
            location="Stadion",
            max_capacity=0,
            date_range=create_valid_event_date()
        )


def test_add_ticket_category_success():
    event_date = create_valid_event_date()
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=event_date
    )
    
    sales_date = create_valid_sales_date(event_date.start_date)
    category = create_valid_ticket_category(quota=50, sales_period=sales_date)
    
    event.add_ticket_category(category)
    assert len(event.categories) == 1

def test_add_ticket_category_fails_when_sales_period_invalid():
    event_date = create_valid_event_date()
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=event_date
    )
    
    invalid_sales_date = DateRange(
        start_date=datetime.now(),
        end_date=event_date.start_date + timedelta(days=2) 
    )
    category = create_valid_ticket_category(quota=50, sales_period=invalid_sales_date)
    
    with pytest.raises(ValueError, match="Ticket sales period must end before or on the event start date."):
        event.add_ticket_category(category)

def test_add_ticket_category_fails_when_quota_exceeds_capacity():
    event_date = create_valid_event_date()
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=event_date
    )
    
    sales_date = create_valid_sales_date(event_date.start_date)
    category1 = create_valid_ticket_category(quota=80, sales_period=sales_date)
    category2 = create_valid_ticket_category(quota=30, sales_period=sales_date)
    
    event.add_ticket_category(category1)
    
    with pytest.raises(ValueError, match="Total ticket quota exceeds event maximum capacity."):
        event.add_ticket_category(category2)


def test_publish_event_success():
    event_date = create_valid_event_date()
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=event_date
    )
    
    sales_date = create_valid_sales_date(event_date.start_date)
    category = create_valid_ticket_category(quota=50, sales_period=sales_date)
    event.add_ticket_category(category)
    
    event.publish()
    assert event.status == EventStatus.PUBLISHED

def test_publish_event_fails_without_active_category():
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=create_valid_event_date()
    )
    
    with pytest.raises(ValueError, match="Event must have at least one active ticket category to be published."):
        event.publish()

def test_cancel_event_success_and_deactivates_tickets():
    event_date = create_valid_event_date()
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=event_date
    )
    
    sales_date = create_valid_sales_date(event_date.start_date)
    category = create_valid_ticket_category(quota=50, sales_period=sales_date)
    event.add_ticket_category(category)
    event.publish()
    
    event.cancel()
    assert event.status == EventStatus.CANCELLED
    assert event.categories[0].is_active is False

def test_cancel_event_fails_when_completed():
    event = Event(
        id=uuid.uuid4(), name="Konser", description="Tes", location="Tes", 
        max_capacity=100, date_range=create_valid_event_date()
    )
    event.status = EventStatus.COMPLETED
    
    with pytest.raises(ValueError, match="Completed events cannot be cancelled."):
        event.cancel()