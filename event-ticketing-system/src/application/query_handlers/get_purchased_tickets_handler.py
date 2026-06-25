from src.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from src.domain.repositories.ticket_repository import TicketRepository

class GetPurchasedTicketsHandler:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def handle(self, query: GetPurchasedTicketsQuery):
        tickets = self.ticket_repository.get_by_customer_id(query.customer_id)
        
        return [
            {
                "id": str(ticket.id),
                "booking_id": str(ticket.booking_id),
                "event_id": str(ticket.event_id),
                "category_id": str(ticket.category_id),
                "code": ticket.code.value,
                "status": ticket.status.value,
                "created_at": ticket.created_at.isoformat() if ticket.created_at else None
            }
            for ticket in tickets
        ]