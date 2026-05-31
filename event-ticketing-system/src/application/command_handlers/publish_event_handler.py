from src.application.commands.publish_event_command import PublishEventCommand
from src.domain.repositories.event_repository import EventRepository

class PublishEventHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: PublishEventCommand) -> None:
        event = self.event_repository.get_by_id(command.event_id)
        if not event:
            raise ValueError("Event not found.")
            
        event.publish()
        self.event_repository.save(event)