import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.repositories.ticket_repository import TicketRepository
from src.domain.aggregates.ticket import Ticket, TicketStatus
from src.domain.value_objects.ticket_code import TicketCode
from src.infrastructure.database.models.ticket_model import TicketModel

class TicketRepositoryImpl(TicketRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, ticket: Ticket) -> None:
        ticket_model = self.session.query(TicketModel).filter_by(id=ticket.id).first()
        
        if not ticket_model:
            ticket_model = TicketModel(id=ticket.id)
            self.session.add(ticket_model)

        ticket_model.code = ticket.code.value
        ticket_model.event_id = ticket.event_id
        ticket_model.category_id = ticket.category_id
        ticket_model.status = ticket.status.value
        ticket_model.created_at = ticket.created_at
        
        if hasattr(ticket, 'booking_id'):
            ticket_model.booking_id = ticket.booking_id

        self.session.commit()

    def get_by_code(self, code: str) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter_by(code=code).first()
        if not model:
            return None

        ticket_code = TicketCode(value=model.code)
        return Ticket(
            id=model.id,
            booking_id=getattr(model, 'booking_id', None),
            event_id=model.event_id,
            category_id=model.category_id,
            code=ticket_code,
            status=TicketStatus(model.status),
            created_at=model.created_at
        )

    def get_by_id(self, ticket_id: uuid.UUID) -> Optional[Ticket]:
        model = self.session.query(TicketModel).filter(TicketModel.id == ticket_id).first()
        if not model:
            return None
            
        ticket_code = TicketCode(value=model.code)
        return Ticket(
            id=model.id,
            booking_id=getattr(model, 'booking_id', None),
            event_id=model.event_id,
            category_id=model.category_id,
            code=ticket_code, 
            status=TicketStatus(model.status),
            created_at=model.created_at
        )

    def get_by_booking_id(self, booking_id: uuid.UUID) -> List[Ticket]:
        models = self.session.query(TicketModel).filter_by(booking_id=booking_id).all()
        tickets = []
        for model in models:
            ticket_code = TicketCode(value=model.code)
            tickets.append(
                Ticket(
                    id=model.id,
                    booking_id=model.booking_id,
                    event_id=model.event_id,
                    category_id=model.category_id,
                    code=ticket_code,
                    status=TicketStatus(model.status),
                    created_at=model.created_at
                )
            )
        return tickets

    def get_by_customer_id(self, customer_id: uuid.UUID) -> List[Ticket]:
        from src.infrastructure.database.models.booking_model import BookingModel
        models = (
            self.session.query(TicketModel)
            .join(BookingModel, TicketModel.booking_id == BookingModel.id)
            .filter(BookingModel.customer_id == customer_id)
            .all()
        )
        tickets = []
        for model in models:
            ticket_code = TicketCode(value=model.code)
            tickets.append(
                Ticket(
                    id=model.id,
                    booking_id=model.booking_id,
                    event_id=model.event_id,
                    category_id=model.category_id,
                    code=ticket_code,
                    status=TicketStatus(model.status),
                    created_at=model.created_at
                )
            )
        return tickets