import uuid
from typing import Optional
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

        self.session.commit()

    def get_by_code(self, code: str) -> Optional[Ticket]:
        ticket_model = self.session.query(TicketModel).filter_by(code=code).first()
        if not ticket_model:
            return None

        ticket_code = TicketCode(value=ticket_model.code)
        ticket = Ticket(
            id=ticket_model.id,
            code=ticket_code,
            event_id=ticket_model.event_id,
            category_id=ticket_model.category_id,
            created_at=ticket_model.created_at
        )
        ticket.status = TicketStatus(ticket_model.status)

        return ticket