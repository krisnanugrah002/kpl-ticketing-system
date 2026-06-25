from src.application.commands.disable_ticket_category_command import DisableTicketCategoryCommand
from src.domain.repositories.event_repository import EventRepository

class DisableTicketCategoryHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: DisableTicketCategoryCommand) -> None:
        event = self.event_repository.get_by_id(command.event_id)
        if not event:
            raise ValueError("Event not found")
        
        event.disable_category(command.category_id)
        self.event_repository.save(event)
        