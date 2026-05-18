import pytest
import uuid
from datetime import datetime, timezone

from src.domain.aggregates.ticket import Ticket, TicketStatus
from src.domain.value_objects.ticket_code import TicketCode

def create_valid_ticket() -> Ticket:
    return Ticket(
        id=uuid.uuid4(),
        booking_id=uuid.uuid4(),
        event_id=uuid.uuid4(),
        category_id=uuid.uuid4(),
        code=TicketCode()
    )

def test_ticket_creation_success():
    ticket = create_valid_ticket()
    
    assert ticket.status == TicketStatus.ACTIVE
    assert isinstance(ticket.code, TicketCode)

def test_check_in_success():
    ticket = create_valid_ticket()
    current_time = datetime.now(timezone.utc)
    
    ticket.check_in(ticket.event_id, current_time)
    
    assert ticket.status == TicketStatus.CHECKED_IN

def test_check_in_fails_when_wrong_event():
    ticket = create_valid_ticket()
    wrong_event_id = uuid.uuid4()
    current_time = datetime.now(timezone.utc)
    
    with pytest.raises(ValueError, match="Ticket is not valid for this event."):
        ticket.check_in(wrong_event_id, current_time)
        
    assert ticket.status == TicketStatus.ACTIVE

def test_check_in_fails_when_already_checked_in():
    ticket = create_valid_ticket()
    current_time = datetime.now(timezone.utc)
    
    ticket.check_in(ticket.event_id, current_time)
    
    with pytest.raises(ValueError, match="Ticket has already been checked in."):
        ticket.check_in(ticket.event_id, current_time)

def test_check_in_fails_when_cancelled():
    ticket = create_valid_ticket()
    current_time = datetime.now(timezone.utc)
    
    ticket.cancel()
    
    with pytest.raises(ValueError, match="Cannot check in a cancelled ticket."):
        ticket.check_in(ticket.event_id, current_time)

def test_cancel_ticket_success():
    ticket = create_valid_ticket()
    
    ticket.cancel()
    
    assert ticket.status == TicketStatus.CANCELLED

def test_cancel_ticket_fails_when_checked_in():
    ticket = create_valid_ticket()
    current_time = datetime.now(timezone.utc)
    
    ticket.check_in(ticket.event_id, current_time)
    
    with pytest.raises(ValueError, match="Cannot cancel a ticket that has already been checked in."):
        ticket.cancel()