import uuid
from src.application.commands.cancel_event_command import CancelEventCommand
from src.domain.repositories.event_repository import EventRepository

class CancelEventHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: CancelEventCommand) -> None:
        event = self.event_repository.get_by_id(command.event_id)
        if not event:
            raise ValueError("Event not found")

        event.cancel()
        self.event_repository.save(event)