from src.application.commands.check_in_command import CheckInCommand
from src.domain.repositories.ticket_repository import TicketRepository

class CheckInHandler:
    def __init__(self, ticket_repository: TicketRepository):
        self.ticket_repository = ticket_repository

    def handle(self, command: CheckInCommand) -> None:
        ticket = self.ticket_repository.get_by_code(command.ticket_code)
        if not ticket:
            raise ValueError("Ticket not found.")
            
        ticket.check_in(command.event_id, command.current_time)
        self.ticket_repository.save(ticket)