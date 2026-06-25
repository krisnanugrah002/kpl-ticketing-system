from src.application.queries.get_purchased_tickets_query import GetPurchasedTicketsQuery
from src.domain.repositories.ticket_repository import TicketRepository

class GetPurchasedTicketsHandler:
    def __init__(self, ticket_repo: TicketRepository):
        self.ticket_repo = ticket_repo

    def handle(self, query: GetPurchasedTicketsQuery) -> list:
        return []