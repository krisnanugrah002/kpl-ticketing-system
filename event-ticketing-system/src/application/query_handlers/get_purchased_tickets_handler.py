from sqlalchemy.orm import Session
from src.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from src.infrastructure.database.models.ticket_model import TicketModel

class GetPurchasedTicketsHandler:
    def __init__(self, session: Session):
        self.session = session

    def handle(self, query: GetPurchasedTicketsQuery):
        tickets = self.session.query(TicketModel).filter(
            TicketModel.booking_id == query.booking_id
        ).all()
        return tickets