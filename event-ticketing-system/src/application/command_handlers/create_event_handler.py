import uuid
from src.application.commands.create_event_command import CreateEventCommand
from src.domain.aggregates.event import Event
from src.domain.entities.ticket_category import TicketCategory
from src.domain.value_objects.date_range import DateRange
from src.domain.value_objects.money import Money
from src.domain.repositories.event_repository import EventRepository
from decimal import Decimal

class CreateEventHandler:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> uuid.UUID:
        event_id = uuid.uuid4()
        event_date_range = DateRange(start_date=command.start_date, end_date=command.end_date)
        
        event = Event(
            id=event_id,
            name=command.name,
            description=command.description,
            location=command.location,
            max_capacity=command.max_capacity,
            date_range=event_date_range
        )
        
        for cat_data in command.categories:
            cat_id = uuid.uuid4()
            cat_sales_period = DateRange(start_date=cat_data.sales_start_date, end_date=cat_data.sales_end_date)
            cat_price = Money(amount=Decimal(str(cat_data.price)))
            
            category = TicketCategory(
                id=cat_id,
                name=cat_data.name,
                price=cat_price,
                quota=cat_data.quota,
                sales_period=cat_sales_period
            )
            event.add_ticket_category(category)
            
        self.event_repository.save(event)
        return event_id